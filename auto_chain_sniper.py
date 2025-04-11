import time
import os
from dotenv import load_dotenv
from solana.keypair import Keypair
from base64 import b64decode
from jupiter_trading import send_sol_transaction
from telegram_bot import send_message

load_dotenv()

TARGET_MINT = os.getenv("SNIPER_MINT")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SNIPER_AMOUNT = float(os.getenv("SNIPER_AMOUNT", 0.01))

# 將 Phantom 匯出的私鑰轉為 Keypair 格式
try:
    decoded = b64decode(PRIVATE_KEY)
    if len(decoded) != 64:
        raise ValueError("私鑰格式錯誤：長度不為 64 bytes")
    keypair = Keypair.from_bytes(decoded)
except Exception as e:
    raise ValueError(f"無法解析私鑰，請確認格式是否正確 (Base64-encoded 64 bytes)：{e}")


def run_sniper():
    print(f"[啟動] 正在掃描目標幣種：{TARGET_MINT}，準備狙擊...")
    send_message(f"🧐 狙擊模式啟動！正在等待 {TARGET_MINT} 上線...", silent=True)

    while True:
        try:
            result = send_sol_transaction(keypair, mint_address=TARGET_MINT, amount_sol=SNIPER_AMOUNT)
            if result:
                print("[成功] 交易成功！TX: ", result)
                send_message(f"🚀 狙擊成功！已購買 {SNIPER_AMOUNT} SOL 到 {TARGET_MINT}\n🔗 TX: https://solscan.io/tx/{result}")
                break
        except Exception as e:
            print("[錯誤] 狙擊失敗：", e)
        time.sleep(5)


if __name__ == '__main__':
    run_sniper()
