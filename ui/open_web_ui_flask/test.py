import requests
import json

# Define the URL of the API
url = 'http://localhost:5000/get-details'

# Define the input to send in the POST request
payload = {
    "input": "HelloWorld"
}

# Set the headers for the request (indicating JSON data)
headers = {
    'Content-Type': 'application/json'
}

# Send a POST request to the API
response = requests.post(url, data=json.dumps(payload), headers=headers)

# Print the response from the API
if response.status_code == 200:
    print("Success!")
    print("Response JSON:", response.json())
else:
    print("Failed with status code:", response.status_code)
    print("Error message:", response.text)
