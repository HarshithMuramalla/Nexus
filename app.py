from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import logging
import os
import random
import time

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for your local frontend (served at http://localhost:5500)
CORS(app, origins=["http://localhost:5500"])

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# App configuration
OLLAMA_API = os.environ.get('OLLAMA_API', "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', "nexus")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            logger.error("No prompt provided in request")
            return jsonify({"error": "No prompt provided"}), 400

        prompt = data['prompt']
        logger.info(f"Received prompt: {prompt}")

        # Construct request payload for Ollama
        ollama_request = {
            "model": OLLAMA_MODEL,
            "messages": [
                { "role": "user", "content": prompt }
            ]
        }

        # Send to Ollama and stream response
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

# Run the Flask app on port 8000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)





