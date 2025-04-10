from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

@app.route('/', methods=['GET'])
def home():
    return "Bot is running."

@app.route('/recommend', methods=['POST'])
def recommend():
    send_message("幣種推薦測試：$SOLA 正在突破，注意低點布局！")
    return "OK"

if __name__ == '__main__':
    app.run()
