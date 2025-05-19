from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import logging
import os
import random
import time

# Initialize Flask app with templates and static folders
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Ollama settings
OLLAMA_API = os.environ.get('OLLAMA_API', "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', "nexus")

# Serve frontend UI
@app.route('/')
def home():
    return render_template('index.html')  # requires templates/index.html

# Handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            logger.error("No prompt provided in request")
            return jsonify({"error": "No prompt provided"}), 400

        prompt = data['prompt']
        logger.info(f"Received prompt: {prompt}")

        ollama_request = {
            "model": OLLAMA_MODEL,
            "messages": [
                { "role": "user", "content": prompt }
            ]
        }

        response = requests.post(OLLAMA_API, json=ollama_request, stream=True)
        logger.info(f"Ollama API status: {response.status_code}")

        if response.status_code == 200:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                        content_piece = chunk.get("message", {}).get("content", "")
                        full_response += content_piece
                    except Exception as e:
                        logger.warning(f"Skipping chunk due to error: {e}")

            logger.info(f"Full assembled response: {full_response}")
            return jsonify({"response": full_response})
        else:
            logger.error(f"Ollama API error: {response.text}")
            return jsonify({"error": "Failed to get response from Ollama"}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

# Start the Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)






