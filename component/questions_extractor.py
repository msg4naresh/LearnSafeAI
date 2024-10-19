import json

def extract_user_questions(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    user_questions = []
    
    for conversation in data:
        for node_id, node in conversation['mapping'].items():
            message = node.get('message')
            if message and message['author']['role'] == 'user':
                content = message['content']['parts'][0]
                user_questions.append(content)
    
    return user_questions
