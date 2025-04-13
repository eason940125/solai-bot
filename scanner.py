import requests

# 自訂條件
MIN_BUYERS = 100
MIN_LIQUIDITY_SOL = 100

def get_new_tokens():
    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/solana"
        res = requests.get(url).json()

        tokens = []

        for item in res.get("pairs", []):
            base_token = item.get("baseToken", {})
            metrics = item.get("metrics", {})

            buyers = item.get("txCount", {}).get("h1", 0)
            liquidity = float(item.get("liquidity", {}).get("usd", 0)) / 25  # rough estimate to SOL
            mint = base_token.get("address", "")
            name = base_token.get("name", "") or base_token.get("symbol", "")

            # 符合條件才列入
            if buyers >= MIN_BUYERS and liquidity >= MIN_LIQUIDITY_SOL:
                tokens.append({
                    "name": name,
                    "address": mint
                })

        return tokens

    except Exception as e:
        print(f"❌ 掃描新幣錯誤：{e}")
        return []
