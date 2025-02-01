from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

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
@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # Handle Preflight Requests
    if request.method == "OPTIONS":
        return jsonify({'message': 'Preflight Request Handled'}), 200

    try:
        user_message = request.json.get('messages', [])

        if not user_message:
            return jsonify({'error': 'Messages parameter is required'}), 400

        data = {
            'model': 'gpt-4o',  # Change model if needed
            'messages': user_message,
        }

        response = requests.post(f'{BASE_URL}/chat/completions', headers=HEADERS, json=data, timeout=TIMEOUT)
        response.raise_for_status()  # Raise error if request fails

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


# Generic API Proxy (Supports GET, POST, PUT, DELETE, OPTIONS)
@app.route('/proxy', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_request():
    # Handle Preflight Requests
    if request.method == "OPTIONS":
        return jsonify({'message': 'Preflight Request Handled'}), 200

    try:
        endpoint = request.args.get('endpoint')  # Example: /chat/completions
        if not endpoint:
            return jsonify({'error': 'Endpoint parameter is required'}), 400

        url = f'{BASE_URL}/{endpoint}'
        method = request.method
        data = request.json if request.data else None

        response = requests.request(method, url, headers=HEADERS, json=data, timeout=TIMEOUT)
        response.raise_for_status()

        return jsonify(response.json())

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

