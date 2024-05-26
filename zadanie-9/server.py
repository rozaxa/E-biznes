from flask import Flask, request, jsonify, send_from_directory
import subprocess
import json
import time
import random

random.seed(time.time())

app = Flask(__name__)

openings = [
    "Hello! How can I assist you today?",
    "Hi there! What are you looking for?",
    "Good day! How can I help you?",
    "Hey! How may I assist you today?",
    "Greetings! How can I be of help today?"
]

closings = [
    "Can I help you with anything else?",
    "Is there anything else I can assist you with today?",
    "Thank you for chatting. See you next time!",
    "I hope I was able to help. Have a great day!",
    "Thank you for using our service. Goodbye!"
]

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('input', '')

    if user_input == "start_chat":
        opening = random.choice(openings)
        return jsonify({'response': opening})
    elif user_input == "end_chat":
        closing = random.choice(closings)
        return jsonify({'response': closing})

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    response = query_llama(user_input)
    return jsonify({'response': response})

def query_llama(input_text):
    ollama_path = "/usr/local/bin/ollama"
    command = [ollama_path, "run", "llama3", input_text]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        try:
            response_data = json.loads(output)
            response_text = response_data.get('text', '')
        except json.JSONDecodeError:
            response_text = output.strip()
        return response_text
    except subprocess.CalledProcessError as e:
        print(f"Error querying LLAMA: {e}")
        return "Error querying LLAMA."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
