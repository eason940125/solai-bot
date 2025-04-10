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
        "text": text,
        "parse_mode": "Markdown"
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
    send_message("*[即時幣種推薦]*\n幣種：$SOLA\n交易量暴增，短線關注機會！")
    return "OK"


    @app.route("/arbitrage_test", methods=["GET"])
def arbitrage_test():
    print("[LOG] /arbitrage_test 被呼叫")
    send_message("🔁 *自動套利偵測啟動*")
    return "Arbitrage test triggered"


@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    print("[LOG] Webhook 收到資料：", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        print(f"[LOG] 收到使用者訊息：{text}，來自 chat_id：{chat_id}")

        if text == "/start":
            send_message("歡迎使用 SolAI_trader_bot！輸入 /recommend 獲取即時推薦。")
        elif text == "/recommend":
            send_message("*[即時幣種推薦]*\n幣種：$SOLA\n交易量暴增，短線關注機會！")
        elif text == "/arbitrage_test":
            send_message("🔁 *自動套利偵測啟動*
正在分析 Solana DEX 報價與流動性差異，偵測跨平台套利機會…")
        elif text == "/help":
            send_message("指令清單：\n/start - 開始使用\n/recommend - 即時推薦幣種\n/arbitrage_test - 啟動套利偵測\n/help - 查看說明")

    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
