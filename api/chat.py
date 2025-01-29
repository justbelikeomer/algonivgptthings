from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # This allows all origins. You can specify specific origins if needed.

API_KEY = 'ddc-EbFxcaUv86HWitMO7ActswKurGHudVq8weN6pOZ8rtPTJnL9KE'
BASE_URL = 'https://api.sree.shop/v1'

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('messages', [])
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'deepseek-r1',  # Change this model as needed
        'messages': user_message,
    }

    try:
        # Call the external API for chat completion
        response = requests.post(f'{BASE_URL}/chat/completions', headers=headers, json=data)
        
        # Return the response from the external API
        return jsonify(response.json())
    
    except Exception as e:
        # Return an error if the external API request fails
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
