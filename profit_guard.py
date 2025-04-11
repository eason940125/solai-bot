# profit_guard.py

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 模擬紀錄（真實應由 tx_log 記錄寫入）
buy_log = {
    # "mint": {"buy_price": 0.0025, "timestamp": 1712726400}
}

# 查詢當前價格（可改用 BirdEye）
def get_price(mint):
    try:
        url = f"https://public-api.birdeye.so/public/price?address={mint}"
        headers = {"X-API-KEY": "demo"}  # 可替換為自己 API Key
        res = requests.get(url, headers=headers)
        return float(res.json()["data"]["value"])
    except:
        return None

# 推播 Telegram 訊息
def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

# 主邏輯：自動止盈止損

def check_profit_stoploss():
    for mint, info in buy_log.items():
        current_price = get_price(mint)
        if current_price is None:
            continue

        buy_price = info["buy_price"]
        pnl = (current_price - buy_price) / buy_price

        if pnl > 1.0:
            send_message(f"🟢 `{mint}` 已漲 +100%，建議止盈 ✅")
        elif pnl < -0.4:
            send_message(f"🔻 `{mint}` 已跌破 -40%，建議止損 ❌")

# 可排程執行（每 3 分鐘）
if __name__ == "__main__":
    while True:
        check_profit_stoploss()
        time.sleep(180)

