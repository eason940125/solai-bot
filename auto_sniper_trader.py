# auto_sniper_trader.py

from flask import Flask, request
import requests
import os
import asyncio
from jupiter_trading import send_sol_transaction, should_sniper

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

SNIPER_TARGET_MINT = os.environ.get("TARGET_MINT")  # 例如 USDC 的 SOL mint
SNIPER_OUTPUT_MINT = os.environ.get("SNIPER_MINT")  # 要搶的幣種 mint
SNIPER_AMOUNT_SOL = float(os.environ.get("SNIPER_AMOUNT", 0.05))
GMGN_ADDRESS = "7u2BdyK9UDWReCkMS4eAsyReHZqYEG2ZgGdXkR2VnHfq"  # 可動態換

# 發送 Telegram 訊息

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"[LOG] 發送訊息: {text}, 回應: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] 發送訊息失敗: {str(e)}")

@app.route("/", methods=["GET"])
def home():
    return "✅ SolAI Sniper Bot 正在運行中..."

@app.route("/snipe", methods=["GET"])
def trigger_sniper():
    print("[SNIPER] 狙擊條件檢查中...")
    if should_sniper(SNIPER_TARGET_MINT, SNIPER_OUTPUT_MINT):
        send_message("🎯 *條件觸發！開始狙擊交易...*")
        tx_result = asyncio.run(send_sol_transaction(GMGN_ADDRESS, SNIPER_AMOUNT_SOL, simulate=False))

        if isinstance(tx_result, dict) and "error" in tx_result:
            send_message(f"❌ 交易失敗：{tx_result['error']}")
        else:
            send_message(f"✅ 狙擊成功！[Solscan 連結](https://solscan.io/tx/{tx_result})")
    else:
        send_message("⚠️ 尚未滿足狙擊條件，稍後再試。")

    return "狙擊流程結束"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
