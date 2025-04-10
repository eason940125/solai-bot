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
    send_message("*幣種推薦實單：*\n$SOLA 正在暴漲中，系統即將進場！")
    # 可加上實際交易邏輯
    return "OK"


@app.route("/test_recommend", methods=["GET"])
def test_recommend():
    print("[LOG] /test_recommend 被呼叫")
    send_message("*[暴漲速報]*\n幣種：$MOONPUMP\n狀態：交易量暴增 +230%\n流動性：132 SOL\n買盤地址激增：+204 個\n建議操作：`短線快進快出`，AI 評分：8.7/10\n提示：具備迷因熱度但持倉風險高，請謹慎入場。")
    send_message("*[每日精選]*\n幣種：$SOLGENIUS\n上線時間：18 小時內\n流動性：405 SOL\n持倉地址成長：+560 個\n建議操作：`中短線關注，有機會連漲`\n技術指標：RSI 58 / MACD 金叉 / NFT 活動熱")
    send_message("*[AI 精選]*\n幣種：$AISIGNAL\n高勝率錢包同步進場：0xA9D...E1F、0xC0F...D91 等共 6 個\n資金集中度：81.3%\n建議策略：`反向跟單 + 設止盈套利`\n模型信心：93.2%，預估高點 +320%")
    return "Test 推播完成"


@app.route("/arbitrage_test", methods=["GET"])
def arbitrage_test():
    print("[LOG] /arbitrage_test 被呼叫")
    send_message("🔁 *套利偵測中*")
    # 這裡你可以加上真實套利演算法觸發邏輯
    return "Arbitrage trigger sent"


@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    print("[LOG] Webhook 收到資料：", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        print(f"[LOG] 收到使用者訊息：{text}，來自 chat_id：{chat_id}")

        if text == "/start":
            send_message("歡迎使用 SolAI_trader_bot！輸入 /recommend 測試推薦功能。")
        elif text == "/recommend":
            send_message("*幣種推薦實單：*\n$SOLA 正在暴漲中，系統即將進場！")
            # 實單交易可在這裡插入交易觸發邏輯
        elif text == "/arbitrage_test":
            send_message("🔁 *套利偵測中*\n開始掃描 Solana DEX 價差與流動性…")
            # 加上套利查詢和下單邏輯
        elif text == "/help":
            send_message("你可以使用 /start、/recommend、/test_recommend、/arbitrage_test 來啟動實際策略。")

    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
