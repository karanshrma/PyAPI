from flask import Flask, jsonify
import google.generativeai as genai

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
    return jsonify(answer=answer)

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
          <p>MEOW MEOW MOEW</p>
        </div>
      </body>
    </html>
    """
    return html_content, 200, {'Content-Type': 'text/html'}

if __name__ == '__main__':
    app.run(debug=True)
