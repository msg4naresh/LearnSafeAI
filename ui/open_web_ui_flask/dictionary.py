from flask import Flask, request, jsonify
from PyDictionary import PyDictionary
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
dictionary = PyDictionary()

@app.route('/meaning', methods=['GET'])
def get_meaning():
    word = request.args.get('word')
    
    # Check if word is provided
    if not word:
        return jsonify({"error": "Please provide a word."}), 400
    
    try:
        # Fetch the meaning from PyDictionary
        meaning = dictionary.meaning(word)
        
        if not meaning:
            return jsonify({"error": "No meaning found for the given word."}), 404
        
        return jsonify({"word": word, "meaning": meaning})
    
    except Exception as e:
        # Return error message in case of any exception
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
