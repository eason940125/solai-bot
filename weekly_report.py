import json
from datetime import datetime, timedelta

LOG_FILE = "tx_record_log.json"

def load_transactions():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def generate_weekly_report():
    transactions = load_transactions()
    if not transactions:
        return "📉 本週無任何交易紀錄。"

    now = datetime.utcnow()
    one_week_ago = now - timedelta(days=7)

    filtered = [
        tx for tx in transactions
        if datetime.fromisoformat(tx["timestamp"]) >= one_week_ago
    ]

    if not filtered:
        return "📉 本週沒有符合條件的交易紀錄。"

    total_tx = len(filtered)
    total_amount = sum(tx["amount_in_sol"] for tx in filtered)
    avg_amount = round(total_amount / total_tx, 4)

    summary = f"""📊 *SolAI 每週交易報表*
週期：{one_week_ago.date()} ~ {now.date()}

✅ 總交易筆數：{total_tx}
💰 總交易金額：{round(total_amount, 4)} SOL
📈 平均每筆投入：{avg_amount} SOL
📦 推薦幣種數量：{len(set(tx["name"] for tx in filtered))}
🧠 AI 命中率：🚧（回測功能未啟用）

可進一步連接行情報酬、漲幅回測、勝率評估（v1.5）"""

    return summary

# 執行測試
if __name__ == "__main__":
    print(generate_weekly_report())
