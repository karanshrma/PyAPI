from flask import Flask, jsonify, request
import google.generativeai as genai
import signal

app = Flask(__name__)

# Configure the genai with your API key
genai.configure(api_key="AIzaSyDx0LELsbJQy6m5zP8_qd5ySfoMjCk9hJo")

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

@app.before_request
def before_request():
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30)  # Set the timeout to 30 seconds

@app.after_request
def after_request(response):
    signal.alarm(0)  # Disable the alarm
    return response

@app.errorhandler(TimeoutException)
def handle_timeout(error):
    return jsonify({'error': 'Request timed out'}), 504

def remove_newlines(text):
    # Replace '\n' and '\r' with an empty string
    cleaned_text = text.replace('\n', '').replace('\r', '')
    return cleaned_text

def chatResponse(messages):
    # Create a new conversation
    response = genai.chat(messages=messages)

    # Last contains the model's response:
    answer = response.last

    # Clean the answer
    cleaned_answer = remove_newlines(answer)

    return cleaned_answer

# Define a route for the URL parameter
@app.route('/api/genai/<message>', methods=['GET'])
def api(message):
    msg = f"{message}"
    answer = chatResponse(msg)
    return jsonify(answer=answer)

@app.route('/api/genai', methods=['GET'])
def api_default():
    return jsonify(error="Message parameter is missing"), 400

# Default
@app.route('/')
def home():
    html_content = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>You are Awesome</title>
      </head>
      <body>
        <div class="container">
          <h1>Welcome to the Flask App!</h1>
          <p>Enter the prompt in URL</p>
        </div>
      </body>
    </html>
    """
    return html_content, 200, {'Content-Type': 'text/html'}

if __name__ == '__main__':
    app.run(debug=True)
