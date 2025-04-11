# weekly_report.py

import os
import json
import requests
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
REPORT_FILE = "tx_record_log.json"  # 假設這是你的交易紀錄儲存檔案

# Helper：傳送 Telegram 推播
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# Helper：載入交易紀錄
def load_tx_log():
    if not os.path.exists(REPORT_FILE):
        return []
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 產生週報
def generate_weekly_report():
    tx_list = load_tx_log()
    now = datetime.utcnow()
    start = now - timedelta(days=7)

    count = 0
    total_gain = 0
    hit_tokens = []
    losses = []

    for tx in tx_list:
        tx_time = datetime.fromtimestamp(tx["timestamp"])
        if tx_time < start:
            continue
        count += 1
        pnl = tx["pnl"]
        if pnl > 0.5:
            hit_tokens.append((tx["symbol"], pnl))
        if pnl < -0.3:
            losses.append((tx["symbol"], pnl))
        total_gain += pnl

    msg = "📊 *策略績效週報*\n\n"
    msg += f"🧾 本週交易次數：{count} 次\n"
    msg += f"💰 總收益評估：{round(total_gain, 2)} SOL\n\n"

    if hit_tokens:
        msg += "🚀 *暴漲命中幣種：*\n"
        for symbol, p in hit_tokens:
            msg += f"• {symbol}: +{int(p*100)}%\n"

    if losses:
        msg += "\n⚠️ *重挫幣種（建議剔除）：*\n"
        for symbol, p in losses:
            msg += f"• {symbol}: {int(p*100)}%\n"

    send_message(msg)

# 可搭配 crontab 或 Render 定時任務自動執行
if __name__ == "__main__":
    generate_weekly_report()
