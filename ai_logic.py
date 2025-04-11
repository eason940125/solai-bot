# ai_logic.py

import random
import os

# 讀取預設倉位上限
try:
    DEFAULT_AMOUNT = float(os.getenv("SNIPER_AMOUNT", 0.05))
except:
    DEFAULT_AMOUNT = 0.05

# 根據 AI 分數決定倉位：
def get_decision(mint):
    # 模擬 AI 信心分數 (0~1)
    score = round(random.uniform(0.5, 1.0), 2)

    # 根據分數動態調整倉位：
    if score >= 0.95:
        amount = DEFAULT_AMOUNT * 2
    elif score >= 0.85:
        amount = DEFAULT_AMOUNT * 1.5
    elif score >= 0.75:
        amount = DEFAULT_AMOUNT
    elif score >= 0.65:
        amount = DEFAULT_AMOUNT * 0.7
    else:
        amount = DEFAULT_AMOUNT * 0.5

    return {
        "amount": round(amount, 4),
        "score": score
    }
