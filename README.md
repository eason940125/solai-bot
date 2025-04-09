# solai-bot
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
    return requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")
    if text == "/start":
        send_message("✅ 成功收到指令！SolAI_trader_bot 正常運作中。")
    return {"ok": True}

app.run(debug=False, host="0.0.0.0", port=8443)
