import json
import os

def extract_user_questions(json_file):
    # Get the absolute path to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct the absolute path to the JSON file
    json_file_path = os.path.join(project_root, 'component', 'data', 'conversations.json')
    
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        user_questions = []
        
        for conversation in data:
            for node_id, node in conversation['mapping'].items():
                message = node.get('message')
                if message and message['author']['role'] == 'user':
                    content = message['content']['parts'][0]
                    user_questions.append(content)
        
        return user_questions
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
