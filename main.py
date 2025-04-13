from flask import Flask, request
from weekly_report import generate_weekly_report
import requests
import os
from dotenv import load_dotenv
from gmgn_trading import buy_token_with_sol

load_dotenv()
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(text, chat_id=CHAT_ID):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        print(f"[訊息發送] {text}")
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
            send_message("👋 歡迎使用 SolAI Bot！輸入 /recommend 開始使用。", chat_id)

        elif text.startswith("/recommend"):
            send_message("📈 幣種推薦測試：\n$SOLA 正在暴漲中，短線可留意。", chat_id)
	elif text.startswith("/weekly"):
    		report = generate_weekly_report()
    		send_message(report, chat_id)


        elif text.startswith("/buy"):
            try:
                _, mint, amount = text.split()
                send_message(f"🚀 準備購買 {amount} SOL 的幣種 {mint}，請稍候...", chat_id)
                tx = buy_token_with_sol(mint, float(amount))
                if isinstance(tx, dict) and "error" in tx:
                    send_message(f"❌ 交易失敗：{tx['error']}", chat_id)
                else:
                    send_message(f"✅ 成功送出交易！\n🔗 https://solscan.io/tx/{tx}", chat_id)
            except Exception as e:
                send_message(f"⚠️ 請使用格式：/buy <Mint> <金額>\n範例：/buy FVeJhMJ... 0.05\n錯誤：{str(e)}", chat_id)

        elif text.startswith("/help"):
            send_message("📋 指令列表：\n/start - 開始使用\n/recommend - 測試推薦\n/buy <Mint> <金額> - 立即買入", chat_id)

        else:
            send_message("🤖 無效指令，請輸入 /help 查看可用指令。", chat_id)

    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
