from flask import Flask, request
import requests
import os
from gmgn_trading import execute_trade
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(text, chat_id=CHAT_ID):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"[訊息發送] {text} 回應: {response.status_code}")
    except Exception as e:
        print(f"[錯誤] 傳送訊息失敗：{e}")

@app.route("/")
def home():
    return "SolAI Bot is Running."

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    print("[Webhook 收到訊息]：", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if text.startswith("/start"):
            send_message("歡迎使用 SolAI_trader_bot！輸入 /recommend 測試推薦功能。", chat_id)
        elif text.startswith("/recommend"):
            send_message("📈 幣種推薦測試：\n$SOLA 正在暴漲中，短線關注！", chat_id)
        elif text.startswith("/help"):
            send_message("指令列表：\n/start - 啟動機器人\n/recommend - 獲取推薦幣種\n/buy 幣種 數量 - 進行交易\n", chat_id)
        elif text.startswith("/buy"):
            try:
                _, symbol, amount = text.split()
                send_message(f"🚀 準備購買 {symbol} 金額 {amount} SOL，請稍候...", chat_id)
                tx_result = execute_trade(symbol.upper(), float(amount))
                if isinstance(tx_result, dict) and "error" in tx_result:
                    send_message(f"❌ 交易失敗：{tx_result['error']}", chat_id)
                else:
                    send_message(f"✅ 成功送出交易！\n🔗 https://solscan.io/tx/{tx_result}", chat_id)
            except Exception as e:
                send_message(f"⚠️ 無法解析 /buy 指令，請使用格式：/buy LHC 0.05\n錯誤：{str(e)}", chat_id)
        else:
            send_message("無效指令，請輸入 /help 查看可用指令。", chat_id)

    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
