import requests
import os
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.rpc.responses import SendTransactionResp
from solana.rpc.api import Client
from base64 import b64decode

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

client = Client(RPC_URL)
keypair = Keypair.from_bytes(b64decode(PRIVATE_KEY))

def send_sol_transaction(output_mint, amount):
    try:
        base_url = "https://quote-api.jup.ag/v6/swap"
        amount_lamports = int(amount * 1e9)

        params = {
            "inputMint": "So11111111111111111111111111111111111111112",  # SOL
            "outputMint": output_mint,
            "amount": amount_lamports,
            "slippageBps": 100,
            "userPublicKey": str(keypair.pubkey()),
            "onlyDirectRoutes": False,
            "simulate": False
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
