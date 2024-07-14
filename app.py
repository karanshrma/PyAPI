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


def chatResponse(messages):
    # Create a new conversation
    response = genai.chat(messages=messages)

    # Last contains the model's response:
    answer = response.last

    return answer


def process_message(message):
    # Handle backspaces
    stack = []
    for char in message:
        if char == '\b':
            if stack:
                stack.pop()
        else:
            stack.append(char)
    processed_message = ''.join(stack)

    # Remove unwanted sequences
    processed_message = processed_message.replace('\r\n\r\n', ' ')  # Replace with a single space or adjust as needed
    return processed_message


# Define a route for the URL parameter
@app.route('/api/genai/<message>', methods=['GET'])
def api(message):
    processed_message = process_message(message)
    response_data = chatResponse(processed_message)
    answer = response_data.get('answer', '')

    # Further clean the answer to remove '\r\n\r\n' sequences
    clean_answer = answer.replace('\r\n\r\n', ' ')

    return jsonify(clean_answer, mimetype='text/plain')


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
        <title>MEOW</title>
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
