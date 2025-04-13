import base64
import requests
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.message import VersionedMessage
from dotenv import load_dotenv
import base58
import os

load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# 讀取 Base58 私鑰並還原 Keypair
def load_keypair_from_base58(b58_str):
    secret = base58.b58decode(b58_str)
    return Keypair.from_bytes(secret)

# 實單下單：SOL 買指定代幣（Mint）
def buy_token_with_sol(mint_address, amount_in_sol):
    try:
        keypair = load_keypair_from_base58(PRIVATE_KEY)
        user_pubkey = keypair.pubkey()

        # 1. 查報價
        amount = int(amount_in_sol * 1e9)
        quote_url = f"https://quote-api.jup.ag/v6/quote?inputMint=So11111111111111111111111111111111111111112&outputMint={mint_address}&amount={amount}&slippageBps=100"
        quote_res = requests.get(quote_url).json()

        if not quote_res.get("data"):
            return {"error": "找不到合適報價"}

        route = quote_res["data"][0]

        # 2. 要求交易
        swap_url = "https://quote-api.jup.ag/v6/swap"
        swap_body = {
            "userPublicKey": str(user_pubkey),
            "wrapUnwrapSOL": True,
            "quoteResponse": route,
            "computeUnitPriceMicroLamports": 10000
        }

        swap_res = requests.post(swap_url, json=swap_body).json()
        swap_tx = swap_res.get("swapTransaction")
        if not swap_tx:
            return {"error": "無法取得交易資訊"}

        # 3. 解碼 tx 並簽名
        tx_bytes = base64.b64decode(swap_tx)
        message = VersionedMessage.deserialize(tx_bytes)
        tx = VersionedTransaction(message, [keypair])
        tx_signed = tx.serialize()

        # 4. 發送到主網
        rpc = "https://api.mainnet-beta.solana.com"
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sendTransaction",
            "params": [base64.b64encode(tx_signed).decode("utf-8")]
        }

        rpc_res = requests.post(rpc, headers=headers, json=payload).json()
        if "result" in rpc_res:
            print("✅ 實單交易成功！TX Hash:", rpc_res["result"])
            return rpc_res["result"]
        else:
            return {"error": rpc_res.get("error", "未知錯誤")}

    except Exception as e:
        return {"error": str(e)}
