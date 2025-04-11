# profit_guard.py

import requests
import os
import time
from solana.rpc.api import Client
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 假設你有記錄買入價格與 mint 到 buy_log 變數中
buy_log = {
    # mint: {'buy_price': 0.0025, 'timestamp': 1680000000}
    # 買入價格是 1 顆該幣種 = 幾 SOL（單位反向）
}

# 取得目前價格（可改為 DEX Screener API）
def get_price(mint):
    try:
        url = f"https://public-api.birdeye.so/public/price?address={mint}"
        headers = {"X-API-KEY": "demo"}  # 可以換成自己 API KEY
        res = requests.get(url, headers=headers)
        return float(res.json()["data"]["value"])
    except:
        return None

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("推播失敗", e)

# 主邏輯：掃描並評估是否止盈或止損
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

# 每 3 分鐘執行一次
if __name__ == "__main__":
    while True:
        check_profit_stoploss()
        time.sleep(180)
