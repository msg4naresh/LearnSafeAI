from typing import List, Dict, TypedDict
from OllamaLlama import OllamaLlama
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuestionGroupInfo(TypedDict):
    category: str
    expertise_rating: int

def retry_with_exponential_backoff(max_retries: int = 3, base_wait: float = 1):
    return retry(
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=base_wait, min=1, max=10),
        reraise=True
    )

class QuestionAnalyzer:
    def __init__(self, adapter: OllamaLlama):
        self.adapter = adapter

    @retry_with_exponential_backoff()
    def categorize_and_rate_questions(self, question_groups: Dict[int, List[str]]) -> Dict[str, QuestionGroupInfo]:
        prompt = f"""
        Analyze the following question groups:
        {question_groups}
        
        For each group:
        1. Assign an appropriate category.
        2. Rate the expertise level on a scale of 1 to 5, where:
           1 - Beginner
           2 - Advanced Beginner
           3 - Intermediate
           4 - Advanced
           5 - Expert

        Respond with a JSON object where keys are group numbers and values are objects containing 'category' and 'expertise_rating'.
        Example:
        {{
            "0": {{"category": "Python Basics", "expertise_rating": 1}},
            "1": {{"category": "Advanced Python", "expertise_rating": 4}}
        }}
        """
        return self.adapter.parse_json_response(self.adapter.chat(prompt))

    @retry_with_exponential_backoff()
    def recommend_concepts(self, categorized_groups: Dict[str, QuestionGroupInfo]) -> Dict[str, List[str]]:
        prompt = f"""
        Based on the following categorized question groups:
        {categorized_groups}
        
        Recommend 3-5 key concepts or topics to study for each category, considering the expertise rating.
        Adapt your recommendations to the specific subject area indicated by the category.
        For lower expertise ratings (1-2), focus on foundational concepts.
        For higher expertise ratings (4-5), suggest more advanced topics.

        Consider the following guidelines:
        - For medical categories, suggest appropriate medical concepts, procedures, or areas of study.
        - For technology categories, recommend relevant technical concepts, tools, or methodologies.
        - For other subjects, adapt your recommendations to fit the specific field or area of study.

        Respond with a JSON object where keys are group numbers and values are lists of recommended concepts.
        Example:
        {{
            "0": ["Basic anatomy", "Medical terminology", "Patient assessment", "Vital signs"],
            "1": ["Advanced diagnostic techniques", "Specialized treatment protocols", "Medical research methodologies"]
        }}
        """
        return self.adapter.parse_json_response(self.adapter.chat(prompt))

class QuestionGrouper:
    def __init__(self, model_name='all-MiniLM-L6-v2', threshold=0.7):
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold

    @retry_with_exponential_backoff()
    def group_similar_questions(self, questions: List[str]) -> Dict[int, List[str]]:
        embeddings = self.model.encode(questions)
        clustering = AgglomerativeClustering(
            n_clusters=None, 
            distance_threshold=self.threshold, 
            metric='cosine', 
            linkage='average'
        ).fit(embeddings)
        
        grouped_questions = {}
        for i, label in enumerate(clustering.labels_):
            grouped_questions.setdefault(label, []).append(questions[i])
        
        for label, group in grouped_questions.items():
            logger.info(f"Group {label}:")
            logger.info("\n".join(f"  - {question}" for question in group))
            logger.info("---")
        
        return grouped_questions

def main(questions: List[str]) -> None:
    adapter = OllamaLlama()
    analyzer = QuestionAnalyzer(adapter)
    grouper = QuestionGrouper()
    
    try:
        grouped_questions = grouper.group_similar_questions(questions)
        logger.info(f"Number of question groups: {len(grouped_questions)}")
        
        categorized_and_rated_groups = analyzer.categorize_and_rate_questions(grouped_questions)
        logger.info(f"Categorized and rated groups: {categorized_and_rated_groups}")
        
        recommended_concepts = analyzer.recommend_concepts(categorized_and_rated_groups)
        for group, concepts in recommended_concepts.items():
            logger.info(f"Group {group}:")
            for concept in concepts:
                logger.info(f"Recommended concept: {concept}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    questions = [
        "How do I install Python?",
        "What's the difference between Python 2 and 3?",
        "How much does your service cost?",
        "Can you explain object-oriented programming?",
        "What's your refund policy?",
        "How do I create a virtual environment in Python?",
    ]
    
    main(questions)
