# === auto_chain_sniper.py ===
import os
import time
from dotenv import load_dotenv
from solders.keypair import Keypair
from base64 import b64decode
from jupiter_trading import send_sol_transaction

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_PUBLIC_KEY = os.getenv("WALLET_PUBLIC_KEY")
RPC_URL = os.getenv("RPC_URL")
SNIPER_MINT = os.getenv("SNIPER_MINT")
SNIPER_AMOUNT = float(os.getenv("SNIPER_AMOUNT", "0.05"))

def run_sniper():
    print(f"[啟動狙擊] 目標代幣: {SNIPER_MINT}, 數量: {SNIPER_AMOUNT} SOL")
    try:
        keypair = Keypair.from_bytes(b64decode(PRIVATE_KEY))
        print("[載入錢包] 成功")
    except Exception as e:
        print(f"[錯誤] 錢包初始化失敗: {e}")
        return

    try:
        print("[發送交易] ...")
        tx = send_sol_transaction(SNIPER_MINT, SNIPER_AMOUNT, keypair, RPC_URL)
        print(f"✅ 實單交易成功！交易 ID: {tx}")
    except Exception as e:
        print(f"❌ 實單交易失敗: {e}")

if __name__ == '__main__':
    run_sniper()


# === requirements.txt ===
flask
requests
python-dotenv
solders==0.11.3
