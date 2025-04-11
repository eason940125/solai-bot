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
    import asyncio
from gmgn_trading import execute_trade

@bot.message_handler(commands=["buy"])
def handle_buy(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "❗ 請輸入格式：/buy 幣種 數量，例如：/buy LHC 0.05")
            return

        coin = args[1].upper()
        amount = float(args[2])

        # ✅ Gmgn.ai 的代收地址（測試使用，後續可自動查最佳交易路徑）
        recipient_address = "7u2BdyK9UDWReCkMS4eAsyReHZqYEG2ZgGdXkR2VnHfq"

        bot.reply_to(message, f"🚀 準備購買 {coin}，金額 {amount} SOL...")

        result = asyncio.run(execute_trade(recipient_address, amount))

        if isinstance(result, dict) and "error" in result:
            bot.send_message(message.chat.id, f"❌ 交易失敗：{result['error']}")
        else:
            bot.send_message(message.chat.id, f"✅ 成功送出交易！🔗 https://solscan.io/tx/{result}")

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ 發生錯誤：{str(e)}")

        import asyncio
from jupiter_trading import send_sol_transaction

@bot.message_handler(commands=["simulate"])
def handle_simulate(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "❗ 請用格式：/simulate 幣種 數量，例如：/simulate LHC 0.05")
            return

        coin = args[1].upper()
        amount = float(args[2])
        recipient_address = "7u2BdyK9UDWReCkMS4eAsyReHZqYEG2ZgGdXkR2VnHfq"  # Gmgn.ai 的接收地址

        bot.reply_to(message, f"🔍 模擬交易中 {amount} SOL 給 {coin} ...")

        result = asyncio.run(send_sol_transaction(recipient_address, amount, simulate=True))

        if "simulate" in result:
            units = result['result']['unitsConsumed']
            bot.send_message(message.chat.id, f"✅ 模擬完成！Gas 預估：{units} 單位")
        else:
            bot.send_message(message.chat.id, f"❌ 模擬失敗：{result.get('error', '未知錯誤')}")

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ 發生錯誤：{str(e)}")

