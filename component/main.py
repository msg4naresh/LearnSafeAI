from typing import List, Dict, Tuple, Optional
from OllamaLlama import OllamaLlama
import time
from httpx import ReadTimeout
import logging
from functools import wraps
from tenacity import retry, stop_after_attempt, wait_exponential

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    def group_similar_questions(self, questions: List[str]) -> Dict[str, List[str]]:
        prompt = f"""
        Group the following questions into similar categories:
        {questions}
        
        Respond with a JSON object where keys are group labels and values are lists of questions.
        """
        response = self.adapter.chat(prompt)
        return self.adapter.parse_json_response(response)

    @retry_with_exponential_backoff()
    def categorize_question_groups(self, question_groups: Dict[str, List[str]]) -> Dict[str, str]:
        prompt = f"""
        Categorize the following question groups into categories like technical, non-technical, billing, or any other appropriate category:
        {question_groups}
        
        Respond with a JSON object where keys are group labels and values are category names.
        """
        response = self.adapter.chat(prompt)
        return self.adapter.parse_json_response(response)

    @retry_with_exponential_backoff()
    def analyze_question_context(self, question: str) -> str:
        prompt = f"""
        Analyze the context of the following question and determine its category:
        {question}
        
        Respond with a single word representing the category.
        """
        return self.adapter.chat(prompt).strip()

    @retry_with_exponential_backoff()
    def identify_knowledge_gaps(self, technical_questions: List[str]) -> List[str]:
        prompt = f"""
        Identify potential knowledge gaps based on these technical questions:
        {technical_questions}
        
        Respond with a JSON array of identified knowledge gap areas.
        """
        response = self.adapter.chat(prompt)
        return self.adapter.parse_json_response(response)

    @retry_with_exponential_backoff()
    def rate_expertise(self, questions: List[str]) -> str:
        prompt = f"""
        Rate the expertise level based on these questions:
        {questions}
        
        Respond with a single word: 'Beginner', 'Intermediate', or 'Advanced'.
        """
        return self.adapter.chat(prompt).strip()

    @retry_with_exponential_backoff()
    def recommend_resources(self, category: str, expertise_level: str, knowledge_gaps: List[str]) -> List[Dict[str, str]]:
        prompt = f"""
        Recommend learning resources for:
        Category: {category}
        Expertise Level: {expertise_level}
        Knowledge Gaps: {knowledge_gaps}
        
        Respond with a JSON array of resource recommendations, including titles and URLs.
        """
        response = self.adapter.chat(prompt)
        return self.adapter.parse_json_response(response)

    def process_questions(self, questions: List[str]) -> Tuple[Dict[str, str], str, List[str], List[Dict[str, str]]]:
        try:
            # Group similar questions
            grouped_questions = self.group_similar_questions(questions)
            logger.info(f"Grouped questions: {grouped_questions}")
            
            # Categorize question groups
            categorized_groups = self.categorize_question_groups(grouped_questions)
            logger.info(f"Categorized groups: {categorized_groups}")
            
            # Rate expertise level
            expertise_level = self.rate_expertise(questions)
            logger.info(f"Expertise level: {expertise_level}")
            
            # Identify knowledge gaps for all questions
            all_questions = [q for group in grouped_questions.values() for q in group]
            knowledge_gaps = self.identify_knowledge_gaps(all_questions)
            logger.info(f"Identified knowledge gaps: {knowledge_gaps}")
            
            # Recommend resources
            primary_category = max(set(categorized_groups.values()), key=list(categorized_groups.values()).count)
            recommended_resources = self.recommend_resources(primary_category, expertise_level, knowledge_gaps)
            logger.info(f"Recommended resources: {recommended_resources}")
            
            return categorized_groups, expertise_level, knowledge_gaps, recommended_resources
        except Exception as e:
            logger.error(f"Error processing questions: {str(e)}")
            raise

def main(questions: List[str]) -> None:
    adapter = OllamaLlama()
    analyzer = QuestionAnalyzer(adapter)
    
    try:
        categorized_groups, expertise_level, knowledge_gaps, recommended_resources = analyzer.process_questions(questions)
        
        print("Categorized Groups:")
        for group, category in categorized_groups.items():
            print(f"{group}: {category}")
        
        print(f"\nExpertise Level: {expertise_level}")
        
        print("\nIdentified Knowledge Gaps:")
        for gap in knowledge_gaps:
            print(f"- {gap}")
        
        print("\nRecommended Resources:")
        if recommended_resources:
            for resource in recommended_resources:
                print(f"- {resource['title']}: {resource['url']}")
        else:
            print("No recommended resources available.")
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