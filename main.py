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


@app.route("/start", methods=["POST", "GET"])
def start():
    print("[LOG] /start 被呼叫")
    send_message("歡迎使用 SolAI_trader_bot！輸入 /recommend 測試推薦功能。")
    return "OK"


@app.route("/recommend", methods=["POST", "GET"])
def recommend():
    print("[LOG] /recommend 被呼叫")
    send_message("*幣種推薦測試：*\n$SOLA 正在暴漲中，短線關注！")
    return "OK"


@app.route("/test_recommend", methods=["GET"])
def test_recommend():
    print("[LOG] /test_recommend 被呼叫")
    send_message("*[暴漲速報]*\n幣種：$MOONPUMP\n狀態：交易量暴增 +230%\n流動性：132 SOL\n買盤地址激增：+204 個\n建議操作：`短線快進快出`，AI 評分：8.7/10\n提示：具備迷因熱度但持倉風險高，請謹慎入場。")
    send_message("*[每日精選]*\n幣種：$SOLGENIUS\n上線時間：18 小時內\n流動性：405 SOL\n持倉地址成長：+560 個\n建議操作：`中短線關注，有機會連漲`\n技術指標：RSI 58 / MACD 金叉 / NFT 活動熱")
    send_message("*[AI 精選]*\n幣種：$AISIGNAL\n高勝率錢包同步進場：0xA9D...E1F、0xC0F...D91 等共 6 個\n資金集中度：81.3%\n建議策略：`反向跟單 + 設止盈套利`\n模型信心：93.2%，預估高點 +320%")
    return "Test 推播完成"


@app.route("/simulate", methods=["GET"])
def simulate():
    print("[LOG] /simulate 被呼叫")
    send_message("📊 模擬下單功能觸發！這只是測試，並未實際送出交易。")
    return "Simulated trade triggered"


@app.route("/buy", methods=["GET"])
def buy():
    print("[LOG] /buy 被呼叫")
    send_message("🟢 真實交易下單請求接收！（尚未實作自動執行）")
    return "Buy command received"


@app.route("/arbitrage_test", methods=["GET"])
def arbitrage_test():
    print("[LOG] /arbitrage_test 被呼叫")
    send_message("🔁 *套利測試啟動*\n正在偵測 Solana DEX 自動套利機會，請稍候…")
    return "Arbitrage test triggered"


@app.route("/price", methods=["GET"])
def price():
    print("[LOG] /price 被呼叫")
    send_message("💱 幣種價格查詢結果：\n$SOL = 165.43（Jupiter）\n$SOL = 165.51（Orca）\n$SOL = 165.47（Raydium）")
    return "Price data returned"


@app.route("/dexinfo", methods=["GET"])
def dexinfo():
    print("[LOG] /dexinfo 被呼叫")
    send_message("📊 支援 DEX 清單：\n- Jupiter\n- Orca\n- Raydium\n- Meteora\n- Lifinity")
    return "DEX info returned"


@app.route("/simulate_arbitrage", methods=["GET"])
def simulate_arbitrage():
    print("[LOG] /simulate_arbitrage 被呼叫")
    send_message("🔬 模擬套利流程：\n1️⃣ Jupiter 買入 $TOKEN 100 USDC\n2️⃣ Raydium 同步賣出 $TOKEN，獲得 106 USDC\n✅ 預估利潤：+6%\n（不包含滑點與 gas 費）")
    return "Arbitrage simulation done"


@app.route("/help", methods=["GET"])
def help():
    print("[LOG] /help 被呼叫")
    help_text = """
🤖 *SolAI_trader_bot 指令說明：*

/start - 啟動機器人
/recommend - 推薦幣種
/test_recommend - 測試幣種卡片
/simulate - 模擬下單
/buy - 真實下單功能
/arbitrage_test - 自動套利測試
/price - 查詢幣價（多平台）
/dexinfo - 顯示支援 DEX
/simulate_arbitrage - 模擬套利流程
/help - 顯示此說明
    """
    send_message(help_text)
    return "Help returned"


@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    print("[LOG] Webhook 收到資料：", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        print(f"[LOG] 收到使用者訊息：{text}，來自 chat_id：{chat_id}")

        if text == "/start":
            send_message("歡迎使用 SolAI_trader_bot！輸入 /recommend 測試推薦功能。")
        elif text == "/recommend":
            recommend()
        elif text == "/test_recommend":
            test_recommend()
        elif text == "/simulate":
            simulate()
        elif text == "/buy":
            buy()
        elif text == "/arbitrage_test":
            arbitrage_test()
        elif text == "/price":
            price()
        elif text == "/dexinfo":
            dexinfo()
        elif text == "/simulate_arbitrage":
            simulate_arbitrage()
        elif text == "/help":
            help()

    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
