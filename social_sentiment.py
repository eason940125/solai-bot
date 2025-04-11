# social_sentiment.py

import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# 推播訊息
def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("推播失敗", e)

# 查詢 Twitter 提及數
def get_twitter_mentions(query):
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    params = {
        "query": query,
        "max_results": 10,
        "tweet.fields": "created_at"
    }
    url = "https://api.twitter.com/2/tweets/search/recent"
    try:
        res = requests.get(url, headers=headers, params=params)
        if res.status_code == 200:
            data = res.json()
            tweets = data.get("data", [])
            return len(tweets)
    except Exception as e:
        print("Twitter 查詢錯誤：", e)
    return 0

# 分析幣種熱度
def check_coin_sentiment(keyword):
    mentions = get_twitter_mentions(keyword)
    if mentions > 5:
        send_message(f"📈 `{keyword}` 社群熱度上升：{mentions} 則推文出現！")
    else:
        print(f"{keyword} 社群推文僅 {mentions} 則，熱度一般")

if __name__ == '__main__':
    keywords = ["$LHC", "$WIF", "$PEPE", "$PUMP"]
    for word in keywords:
        check_coin_sentiment(word)
        time.sleep(2)
