from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# API Configuration
API_KEY = 'ddc-EbFxcaUv86HWitMO7ActswKurGHudVq8weN6pOZ8rtPTJnL9KE'
BASE_URL = 'https://api.sree.shop/v1'

# Default Headers
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

# Timeout Settings
TIMEOUT = 60  # 60 seconds


# Handle Chat Requests (Supports POST)
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Log the raw request for debugging
        print("Received request:", request.data)

        # Ensure the request contains valid JSON
        if not request.is_json:
            return jsonify({'error': 'Invalid JSON format'}), 400

        data = request.get_json()
        print("Parsed JSON:", data)

        user_message = data.get('messages')

        if not isinstance(user_message, list) or not user_message:
            return jsonify({'error': 'Messages parameter must be a non-empty list'}), 400

        payload = {
            'model': 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B\n',  # Change model if needed
            'messages': user_message,
        }

        response = requests.post(f'{BASE_URL}/chat/completions', headers=HEADERS, json=payload, timeout=TIMEOUT)
        response.raise_for_status()  # Raise error if request fails

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
