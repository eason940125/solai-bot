# jupiter_trading.py

import requests
import os
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.rpc.responses import SendTransactionResp
from solana.rpc.api import Client
from base64 import b64decode
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
client = Client(RPC_URL)

# 載入錢包金鑰
keypair = Keypair.from_bytes(b64decode(PRIVATE_KEY))

# 檢查是否有 SOL->token 的 Swap 路徑

def should_sniper(input_mint, output_mint):
    try:
        url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount=10000000&slippage=1"
        res = requests.get(url)
        if res.status_code == 200 and res.json().get("data"):
            return True
    except:
        pass
    return False

# 真實送出交易

def send_sol_transaction(output_mint, amount, simulate=False):
    try:
        base_url = "https://quote-api.jup.ag/v6/swap"
        amount_lamports = int(amount * 1e9)
        params = {
            "inputMint": "So11111111111111111111111111111111111111112",
            "outputMint": output_mint,
            "amount": amount_lamports,
            "slippageBps": 100,
            "userPublicKey": str(keypair.pubkey()),
            "onlyDirectRoutes": False,
            "simulate": simulate
        }
        quote = requests.post(base_url, json=params).json()

        tx = quote["swapTransaction"]
        tx_bytes = b64decode(tx)
        from solders.transaction import VersionedTransaction
        txn = VersionedTransaction.from_bytes(tx_bytes)
        txn.sign([keypair])

        txid = client.send_raw_transaction(txn.serialize(), opts={"skip_preflight": True})
        return txid.value if isinstance(txid, SendTransactionResp) else txid

    except Exception as e:
        return {"error": str(e)}
