# gmgn_trading.py

import os
import base64
from solana.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.rpc.types import TxOpts
from solana.system_program import transfer, TransferParams
from solders.pubkey import Pubkey
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

def get_keypair():
    decoded = base64.b64decode(PRIVATE_KEY)
    return Keypair.from_secret_key(decoded)

async def execute_trade(recipient_address: str, amount_sol: float):
    client = AsyncClient(RPC_URL)
    keypair = get_keypair()
    lamports = int(amount_sol * 1_000_000_000)

    tx = Transaction()
    tx.add(
        transfer(
            TransferParams(
                from_pubkey=keypair.public_key,
                to_pubkey=Pubkey.from_string(recipient_address),
                lamports=lamports
            )
        )
    )

    try:
        response = await client.send_transaction(tx, keypair, opts=TxOpts(skip_preflight=True))
        await client.close()
        return response.value  # 返回 tx hash
    except Exception as e:
        await client.close()
        return {"error": str(e)}
