from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get-details', methods=['POST'])
def get_details():
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    # Get the data from the request
    data = request.get_json()
    
    # Validate the input
    if 'input' not in data:
        return jsonify({"error": "Missing 'input' field in JSON data"}), 400
    
    user_input = data['input']
    
    # Generate some details based on the user input
    details = {
        "input": user_input,
        "length_of_input": len(user_input),
        "uppercase_version": user_input.upper(),
        "is_alpha": user_input.isalpha(),
        "reversed": user_input[::-1]
    }
    
    # Return the details as a JSON response
    return jsonify(details), 200

if __name__ == '__main__':
    app.run(debug=True)
