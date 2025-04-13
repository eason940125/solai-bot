import time
from scanner import get_new_tokens
from gmgn_trading import buy_token_with_sol
from tx_logger import log_transaction

AMOUNT_IN_SOL = 0.05  # 每筆購買 SOL 數量
SCAN_INTERVAL = 5     # 掃描間隔（秒）

def run_sniper_once():
    try:
        tokens = get_new_tokens()
        if not tokens:
            print("❌ 沒有符合條件的新幣")
            return

        for token in tokens:
            name = token["name"]
            mint = token["address"]

            print(f"🎯 發現目標幣種：{name}（{mint}）")
            tx = buy_token_with_sol(mint, AMOUNT_IN_SOL)

            if isinstance(tx, dict) and "error" in tx:
                print(f"❌ 狙擊失敗：{name}\n錯誤：{tx['error']}")
            else:
                print(f"""✅ 成功狙擊：
幣種：{name}
Mint：{mint}
數量：{AMOUNT_IN_SOL} SOL
交易哈希：https://solscan.io/tx/{tx}
""")
                log_transaction(name, mint, AMOUNT_IN_SOL, tx)

    except Exception as e:
        print(f"❌ 系統錯誤：{e}")

# 主執行循環
if __name__ == "__main__":
    print("🔁 啟動 SolAI Sniper 自動狙擊模組")
    while True:
        run_sniper_once()
        time.sleep(SCAN_INTERVAL)
