
from flask import Flask, request, jsonify, render_template
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("OPENAI_API_KEY")


def get_ai_response(msg):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an academic advisor chatbot"},
                {"role": "user", "content": msg}
            ]
        }
    )

    data = response.json()

    # SAFE CHECK
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {data.get('error', {}).get('message', 'Unknown error')}"
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message")
    reply = get_ai_response(msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)