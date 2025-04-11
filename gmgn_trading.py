# gmgn_trading.py

import os
from base64 import b64decode
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
client = Client(RPC_URL)
keypair = Keypair.from_bytes(b64decode(PRIVATE_KEY))

# 發送 SOL 至指定地址（基礎版本）
def execute_trade(recipient_address, amount):
    try:
        tx = transfer(
            TransferParams(
                from_pubkey=keypair.pubkey(),
                to_pubkey=Pubkey.from_string(recipient_address),
                lamports=int(amount * 1e9)
            )
        )
        latest_blockhash = client.get_latest_blockhash()["result"]["value"]["blockhash"]
        from solana.transaction import Transaction
        transaction = Transaction(recent_blockhash=latest_blockhash, fee_payer=keypair.pubkey())
        transaction.add(tx)
        transaction.sign(keypair)
        result = client.send_raw_transaction(transaction.serialize())
        return result["result"]
    except Exception as e:
        return {"error": str(e)}
