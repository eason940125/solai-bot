import os
import base64
import requests
import json
from solana.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.rpc.types import TxOpts
from solana.system_program import transfer, TransferParams
from solders.pubkey import Pubkey
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SLIPPAGE = 1  # 預設 1%
LOG_FILE = "trade_log.json"

# 查詢最佳 swap 路徑（使用 Jupiter Aggregator）
def get_best_swap_route(input_mint, output_mint, amount):
    url = "https://quote-api.jup.ag/v6/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": str(amount),
        "slippageBps": str(SLIPPAGE * 100)
    }
    response = requests.get(url, params=params)
    return response.json()

# 預估可獲得的 token 數量
def estimate_received_token(input_mint, output_mint, amount):
    result = get_best_swap_route(input_mint, output_mint, amount)
    if "data" in result and len(result["data"]) > 0:
        route = result["data"][0]
        out_amount = int(route["outAmount"]) / (10 ** int(route["outToken"]["decimals"]))
        return out_amount
    return None

# 紀錄交易
def log_trade(result, recipient, amount, simulate):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "recipient": recipient,
        "amount": amount,
        "simulate": simulate,
        "result": result
    }
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(record)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# 取得 Keypair
def get_keypair():
    decoded = base64.b64decode(PRIVATE_KEY)
    return Keypair.from_secret_key(decoded)

# 發送交易（simulate = True 為模擬模式）
async def send_sol_transaction(recipient_address: str, amount_sol: float, simulate=False):
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
        if simulate:
            sim_result = await client.simulate_transaction(tx, sig_verify=False)
            await client.close()
            log_trade(sim_result.value, recipient_address, amount_sol, True)
            return {"simulate": True, "result": sim_result.value}
        else:
            result = await client.send_transaction(tx, keypair, opts=TxOpts(skip_preflight=True))
            await client.close()
            log_trade(result.value, recipient_address, amount_sol, False)
            return result.value
    except Exception as e:
        await client.close()
        log_trade({"error": str(e)}, recipient_address, amount_sol, simulate)
        return {"error": str(e)}

# 自動狙擊觸發（當偵測新幣時）
def should_sniper(input_mint, output_mint):
    try:
        result = get_best_swap_route(input_mint, output_mint, 10000000)  # 0.01 SOL
        if "data" in result and len(result["data"]) > 0:
            return True
    except:
        return False
    return False
