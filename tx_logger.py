import json
import os

LOG_FILE = "tx_record_log.json"

def log_transaction(data):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
        print("📝 TX 已記錄 tx_record_log.json")

    except Exception as e:
        print(f"⚠️ 寫入交易紀錄時錯誤: {e}")
