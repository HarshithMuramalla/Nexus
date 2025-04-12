from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import logging
import os
import random
import time

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for your Vercel frontend
CORS(app, origins=["https://nexus-kappa-pearl.vercel.app"])

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# App configuration
OLLAMA_API = os.environ.get('OLLAMA_API', "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', "nexus")
USE_MOCK_RESPONSES = os.environ.get('USE_MOCK_RESPONSES', 'false').lower() == 'true'

# Mock demo responses
SAMPLE_RESPONSES = [
    "I'm a simulated response since Ollama isn't connected. In a real setup, I would pass your query to the Ollama API!",
    "Hello! This is a demonstration of the chat interface. Your actual Ollama model would provide real responses here.",
    "The interface is fully functional, but I'm just a mock responder since we're not connected to Ollama. Nice UI though, right?",
    "If you had Ollama running locally, you'd get an actual AI response here. For now, I'm just showing off the interface capabilities!",
    "This is a placeholder response. In production, your message would be sent to Ollama running on port 11434.",
    "I'm demonstrating how the chat interface works. All features are functional, but responses are pre-written without Ollama.",
    "In a real setup, your message would be processed by Ollama. For now, enjoy this simulated response!",
]

@app.route('/')
def home():
    mode = "Demo Mode" if USE_MOCK_RESPONSES else f"Ollama: {OLLAMA_MODEL}"
    return render_template('index.html', mode=mode, model=OLLAMA_MODEL)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            logger.error("No prompt provided in request")
            return jsonify({"error": "No prompt provided"}), 400

        prompt = data['prompt']
        logger.info(f"Received prompt: {prompt}")

        if USE_MOCK_RESPONSES:
            time.sleep(1)
            response_text = random.choice(SAMPLE_RESPONSES)
            logger.info(f"Mock response: {response_text}")
            return jsonify({"response": response_text})

        ollama_request = {
            "model": OLLAMA_MODEL,
            "messages": [
                { "role": "user", "content": prompt }
            ]
        }

        # Streamed request to Ollama
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)



