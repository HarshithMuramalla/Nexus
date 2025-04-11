from flask import Flask, request, jsonify, render_template
import requests
import json
import logging
import os
import random
import time

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# App configuration
OLLAMA_API = os.environ.get('OLLAMA_API', "https://79e0-174-93-238-64.ngrok-free.app/api/chat")
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', "nexus")
# Set to False by default to connect to the real Ollama server
USE_MOCK_RESPONSES = os.environ.get('USE_MOCK_RESPONSES', 'false').lower() == 'true'

# Fun sample responses for demo mode
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
    """Render the chat interface"""
    # Pass mode and model information to the template
    mode = "Demo Mode" if USE_MOCK_RESPONSES else f"Ollama: {OLLAMA_MODEL}"
    return render_template('index.html', mode=mode, model=OLLAMA_MODEL)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            logger.error("No prompt provided in request")
            return jsonify({"error": "No prompt provided"}), 400

        prompt = data['prompt']
        logger.info(f"Received prompt: {prompt}")

        # Check if we're using mock responses
        if USE_MOCK_RESPONSES:
            # Simulate thinking time
            time.sleep(1)
            response_text = random.choice(SAMPLE_RESPONSES)
            
            # Add contextual prefix if possible
            if "name" in prompt.lower() or "who are you" in prompt.lower():
                response_text = "I'm Nexus, an AI assistant interface. " + response_text
            elif "hello" in prompt.lower() or "hi" in prompt.lower():
                response_text = "Hello there! " + response_text
            elif "help" in prompt.lower():
                response_text = "I'd be happy to help! " + response_text
            elif "thank" in prompt.lower():
                response_text = "You're welcome! " + response_text
            
            logger.info(f"Mock response: {response_text}")
            return jsonify({"response": response_text})
        
        # If not using mock, try to connect to Ollama
        # Prepare the request to Ollama
        ollama_request = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        # Send request to Ollama and handle streaming response
        response = requests.post(OLLAMA_API, json=ollama_request, stream=True)

        if response.status_code == 200:
            full_response = ""
            for chunk in response.iter_lines():
                if chunk:
                    chunk_data = json.loads(chunk.decode('utf-8'))
                    message_content = chunk_data.get("message", {}).get("content", "")
                    full_response += message_content

            logger.info(f"Full response from Ollama: {full_response}")
            return jsonify({"response": full_response})
        else:
            logger.error(f"Ollama API error: {response.text}")
            return jsonify({"error": "Failed to get response from Ollama"}), 500

    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to Ollama server at {OLLAMA_API}. Make sure it's running and accessible."
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 503
        
    except requests.exceptions.Timeout:
        error_msg = "Request to Ollama server timed out. The server might be busy or unresponsive."
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 504
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to Ollama: {str(e)}"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500
        
    except json.JSONDecodeError:
        error_msg = "Failed to parse response from Ollama server. The response format may have changed."
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
