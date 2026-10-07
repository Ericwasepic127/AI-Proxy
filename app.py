import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Fetch the OpenRouter API key from environment variables for security
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    # 1. Grab the full messages array from the incoming request payload
    user_messages = request.json.get("messages") 
    
    if not user_messages or not isinstance(user_messages, list):
        return jsonify({"error": "A 'messages' array is required"}), 400
        
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "Server configuration error: Missing API Key"}), 500

    # 2. FIXED: Configure the correct, specific API endpoint path
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openrouter/free", # Valid router for zero-cost models
        "messages": user_messages
    }

    try:
        # 3. Forward the request to OpenRouter
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        # Check if OpenRouter returned an API error directly
        if "error" in response_data:
            return jsonify({"error": response_data["error"]}), response.status_code
        
        # 4. FIXED: Extract using exact index mapping from OpenRouter's payload format
        ai_response = response_data['choices'][0]['message']['content']
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": f"Internal proxy error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
