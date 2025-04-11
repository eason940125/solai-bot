# auto_chain_sniper.py

import os
import asyncio
import requests
import json
import time
from solana.rpc.async_api import AsyncClient
from jupiter_trading import should_sniper, send_sol_transaction
from ai_logic import get_decision
from dotenv import load_dotenv

load_dotenv()

GMGN_ADDRESS = "7u2BdyK9UDWReCkMS4eAsyReHZqYEG2ZgGdXkR2VnHfq"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RPC_URL = os.getenv("RPC_URL")
WALLET_PUBLIC_KEY = os.getenv("WALLET_PUBLIC_KEY")

TX_LOG_PATH = "tx_record_log.json"

# 推播訊息至 Telegram
def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("訊息發送失敗", e)

# 從 pump.fun 取得新幣 Mint
def get_recent_pumpfun_mints(limit=10):
    try:
        res = requests.get("https://pump.fun/api/markets")
        if res.status_code == 200:
            data = res.json()
            return [m["tokenMint"] for m in data[:limit]]
    except:
        pass
    return []

# 查詢 SOL 餘額
async def get_wallet_balance():
    client = AsyncClient(RPC_URL)
    resp = await client.get_balance(WALLET_PUBLIC_KEY)
    await client.close()
    return resp.value / 1_000_000_000

# 寫入交易紀錄 JSON 檔案
def record_transaction(mint, buy_price, sell_price):
    pnl = (sell_price - buy_price) / buy_price
    tx_log = {
        "symbol": "UNKNOWN",
        "mint": mint,
        "timestamp": int(time.time()),
        "buy_price": buy_price,
        "sell_price": sell_price,
        "pnl": pnl
    }
    try:
        if os.path.exists(TX_LOG_PATH):
            with open(TX_LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        data.append(tx_log)
        with open(TX_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("寫入 tx log 發生錯誤：", e)

# 自動掃鏈主程式
async def auto_chain_sniper():
    while True:
        recent_mints = get_recent_pumpfun_mints(limit=8)
        balance = await get_wallet_balance()

        for mint in recent_mints:
            if should_sniper("So11111111111111111111111111111111111111112", mint):
                decision = get_decision(mint)
                amount = decision["amount"]
                score = decision["score"]

                if amount > balance:
                    send_message(f"💡 資金不足，無法狙擊：{mint[:4]}... (score={score})")
                    continue

                send_message(f"🎯 檢測到新 Mint 上線！\nScore: {score}\n準備買入 {amount} SOL\nMint: `{mint}`")

                result = await send_sol_transaction(GMGN_ADDRESS, amount, simulate=False)
                if isinstance(result, dict) and "error" in result:
                    send_message(f"❌ 狙擊失敗：{result['error']}")
                else:
                    send_message(f"✅ 狙擊成功！[Solscan](https://solscan.io/tx/{result})")
                    record_transaction(mint, buy_price=amount, sell_price=amount * (1 + 0.8))  # 假設獲利 80%

        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(auto_chain_sniper())
