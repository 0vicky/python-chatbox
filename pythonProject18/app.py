import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def chat_gpt_api_call(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <CHATGPT_API_KEY>",
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpdesk assistant."},
            {"role": "user", "content": message},
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    reply = "Sorry, I couldn't generate a response. Please try again."

    if "choices" in response_json and len(response_json["choices"]) > 0:
        choices = response_json["choices"]
        for choice in choices:
            if "message" in choice and "content" in choice["message"]:
                reply = choice["message"]["content"]
                break

    return reply

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    message = request.json["message"]
    response = chat_gpt_api_call(message)
    return {"reply": response}

if __name__ == "__main__":
    app.run()
