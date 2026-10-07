import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

when = """<title>This is AI Proxy Server by Ericwasepic127</title>
<h1>This is AI Proxy Server by Ericwasepic127</h1>
<hr>
<p>Use POST to get API response</p>
<br>
<strong>Or else, you will end up here</strong>"""

app = Flask(__name__)
CORS(app)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/ready', methods=['GET'])
def ready():
     return "ok\n", 200

@app.route('/', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':
        return when, 200
    model = request.json.get("model", os.environ.get("OPENROUTER_MODEL", "openrouter/free"))
    user_messages = request.json.get("messages") 
    if not user_messages or not isinstance(user_messages, list):
        return jsonify({"error": "A 'messages' array is required"}), 400
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "Server configuration error: Missing API Key"}), 500
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": user_messages
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        if "error" in response_data:
            return jsonify({"error": response_data["error"]}), response.status_code
        ai_response = response_data['choices'][0]['message']['content']
        return jsonify({"response": ai_response})
    except (BaseException, Exception) as e:
        return jsonify({"error": f"Internal proxy error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443 if getattr(os, "getuid", lambda: 1000)() == 0 else os.environ.get("AI_PORT", 5000))
