from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7189095135:AAGRYeXwIxxt-ry08KuUJOofO2Hk8ckDsLc"
CHAT_ID = "1958974364"

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
    send_message("幣種推薦測試：$SOLA 正在暴漲，進場條件符合！")
    return "OK"

if __name__ == '__main__':
    app.run()