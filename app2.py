#!/usr/bin/env python3
# Made by @Ericwasepic127

# IMPORTS
import flask, requests, os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

# VARIABLES
GETWARN = """<title>AI Proxy Server by Ericwasepic127</title>
<h1>This is AI Proxy Server by Ericwasepic127</h1>
<hr>
<p>Use POST to get API response</p>
<br>
<strong>Or else, you will end up here</strong>"""
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")  
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
LIMIT = int(os.environ.get("LIMIT", "4"))
COUNT= 0
PROVIDERS = {
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "key_env": GROQ_API_KEY,
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "minimaxai/minimax-m2.7",
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
            "whisper-large-v3",
            "whisper-large-v3-turbo",
        ],
    },
    "gemini": {
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "key_env": GEMINI_API_KEY,
        "models": [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-3.7-flash",
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemma-4-31b-it",
            "gemma-4-26b-a4b-it",
            "gemini-flash-latest",
            "gemini-3.8-flash",
        ],
    },
    "openrouter": {
                "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": OPENROUTER_API_KEY,
        "models": [
            "openrouter/free",
        ],
    },
}

# HELPERS /FUNCTIONS/
def post(url, key, data):
    try:
        r = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=data
        )
        return r.text, r.status_code
    except (BaseException, Exception) as e:
        return jsonify({"error": {
            "message": str(e),
            "type":"api_error",
            "code": type(e).__name__
            }
        }), 500

def handleReq(f):
    global COUNT
    def w(*a, **k):
        global COUNT
        COUNT += 1
        try:
            s = f(*a, **k)
        except:
            s = None
        else:
            return s
        finally:
            COUNT -= 1
    return w

# PREPARE
app = Flask(__name__)
CORS(app)

# HANDLERS
@app.route('/ready', methods=['GET'])
def ready():
     return "ok\n", 200

@app.route('/', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':
        return when, 200
