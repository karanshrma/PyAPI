from flask import Flask, jsonify
import google.generativeai as genai

app = Flask(__name__)

import gemini_api
from flask import Flask, jsonify
import google.generativeai as genai

# Initialize the Flask application
app = Flask(__name__)

# Configure the genai with your API key
genai.configure(api_key="AIzaSyDx0LELsbJQy6m5zP8_qd5ySfoMjCk9hJo")

def chatResponse(messages):
    # Create a new conversation
    response = genai.chat(messages=messages)

    # Last contains the model's response:
    answer = response.last

    return answer

# Define a route for the URL parameter
@app.route('/api/genai/<message>', methods=['GET'])
def api(message):
    msg = f"Hello, {message}!"
    answer = chatResponse(msg)
    return answer
if __name__ == '__main__':
    app.run(debug=True)
