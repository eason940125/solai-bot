from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.rpc.requests import SendTransaction
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from base64 import b64decode
import os

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

client = Client(RPC_URL)

def get_keypair():
    try:
        decoded = b64decode(PRIVATE_KEY)
        if len(decoded) != 64:
            raise ValueError(f"Keypair must be 64 bytes, got {len(decoded)}")
        return Keypair.from_bytes(decoded)
    except Exception as e:
        print(f"[錯誤] 無法解析私鑰：{e}")
        raise

def execute_trade(symbol: str, amount: float):
    try:
        keypair = get_keypair()
        sender_pubkey = keypair.pubkey()

        # 此範例示範將 SOL 轉給自己（測試用），實際上可改為 DEX swap 模組
        tx = Transaction()
        tx.add(
            transfer(
                TransferParams(
                    from_pubkey=sender_pubkey,
                    to_pubkey=sender_pubkey,
                    lamports=int(amount * 1_000_000_000),
                )
            )
        )

        response = client.send_transaction(tx, keypair)
        print("[交易已送出]", response)
        return response["result"]
    except Exception as e:
        print(f"[錯誤] 交易發送失敗：{e}")
        return {"error": str(e)}
