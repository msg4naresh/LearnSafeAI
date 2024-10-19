from typing import List, Dict, TypedDict, Any
from OllamaLlama import OllamaLlama
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
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
    def analyze_questions_and_recommend_concepts(self, question_group: List[str]) -> Dict[str, Any]:
        prompt = f"""
        Based on the following group of questions:
        {question_group}

        1. Identify the main topic or subject of these questions.
        2. Assess the user's expertise level on a scale of 1-5, where:
           1 = Beginner
           2 = Elementary
           3 = Intermediate
           4 = Advanced
           5 = Expert
        3. Identify knowledge gaps based on the complexity and depth of the questions.
        4. Recommend 2-3 key concepts or topics to study, considering the user's expertise level.
           For lower expertise levels (1-2), focus on foundational concepts.
           For higher expertise levels (4-5), suggest more advanced topics.

        Respond with a JSON object containing the following keys:
        - "category": Name of the identified category
        - "expertise_level": Assessed expertise level (1-5)
        - "knowledge_gaps": List of identified knowledge gaps
        - "recommendations": List of recommended concepts to study

        Example response:
        {{
            "category": "Medical Diagnosis",
            "expertise_level": 3,
            "knowledge_gaps": ["Advanced imaging techniques", "Rare disease identification"],
            "recommendations": ["MRI and CT scan interpretation", "Diagnostic algorithms for rare diseases", "Latest advancements in medical imaging"]
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
        
        print("\n" + "="*50)
        print("Question Grouping Results:")
        print("="*50)
        for label, group in grouped_questions.items():
            print(f"\nGroup {label}:")
            for question in group:
                print(f"  - {question}")
        print("="*50 + "\n")
        
        return grouped_questions

def main(questions: List[str]) -> None:
    adapter = OllamaLlama()
    analyzer = QuestionAnalyzer(adapter)
    grouper = QuestionGrouper()
    
    try:
        grouped_questions = grouper.group_similar_questions(questions)
        print(f"\nNumber of question groups: {len(grouped_questions)}\n")
        
        for group_id, questions in grouped_questions.items():
            print(f"\n{'='*50}")
            print(f"Analyzing Group {group_id}:")
            print(f"{'='*50}")
            print("Questions in this group:")
            for question in questions:
                print(f"  - {question}")
            print("\nRecommendations:")
            recommended_concepts = analyzer.analyze_questions_and_recommend_concepts(questions)
            print(json.dumps(recommended_concepts, indent=2))
            print(f"{'='*50}\n")
        
    except Exception as e:
        print(f"\nError: An error occurred: {str(e)}")

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
