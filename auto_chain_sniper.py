# auto_chain_sniper.py（正式交易版）

import requests
import os
import time
from jupiter_trading import send_sol_transaction
from ai_logic import score_coin
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SNIPER_AMOUNT = float(os.getenv("SNIPER_AMOUNT", 0.05))

PUMP_FUN_LIST_URL = "https://client-api-2-1ebf686d2a32.herokuapp.com/all-tokens"

# 推播通知
def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("推播錯誤：", e)

# 掃描 pump.fun 資料
def fetch_pump_list():
    try:
        res = requests.get(PUMP_FUN_LIST_URL, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print("取得 pump.fun 清單失敗：", e)
    return []

# 主邏輯：找新幣 + 分數高就真實下單
def run_sniper():
    seen = set()
    print("🚀 自動狙擊啟動中...")

    while True:
        tokens = fetch_pump_list()
        for t in tokens:
            symbol = t.get("symbol")
            mint = t.get("mint")
            created = t.get("created")

            if not mint or mint in seen:
                continue

            score = score_coin(t)
            if score < 0.75:
                continue

            position = SNIPER_AMOUNT * (1.5 if score >= 0.9 else 1.0)

            # 執行真實下單
            tx = send_sol_transaction(mint, position)
            tx_link = f"https://solscan.io/tx/{tx}" if isinstance(tx, str) else "交易失敗"

            # 發送推播
            send_message(f"🔥 *發現潛力新幣* {symbol}\n分數：{round(score, 2)}\nMint: `{mint}`\n實單買入 {position} SOL\n🔗 {tx_link}")

            seen.add(mint)
            time.sleep(2)

        time.sleep(15)  # 每 15 秒掃描一次

if __name__ == '__main__':
    run_sniper(
