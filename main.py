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
    response = requests.post(url, json=payload)
    print(f"[LOG] 發送訊息: {text}, 回應: {response.status_code} - {response.text}")

@app.route("/", methods=["GET"])
def home():
    print("[LOG] GET / 被呼叫")
    return "Bot is running."

@app.route("/recommend", methods=["POST", "GET"])
def recommend():
    print("[LOG] /recommend 被呼叫")
    send_message("幣種推薦測試：$SOLA 正在暴漲中，短線關注！")
    return "OK"

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    print("[LOG] Webhook 收到資料：", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        print(f"[LOG] 收到使用者訊息：{text}，來自 chat_id：{chat_id}")

        if text == "/recommend":
            send_message("這是 AI 推薦幣種的測試回應。")
        elif text == "/start":
            send_message("歡迎使用 SolAI_trader_bot！輸入 /recommend 看推薦幣。")
        elif text == "/help":
            send_message("你可以使用 /start, /recommend 來測試機器人。")

    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
