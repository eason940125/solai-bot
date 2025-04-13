from solders.keypair import Keypair
import base58

print("=== Start Base58 Key Validation ===")

try:
    # 在這裡貼上你要驗證的 Base58 私鑰
    base58_key = "5vQxKoDumwolbe9gHqi3uWBJpzScNoAn8TkZQPlWCiKnYpPw2efycjsnu95cGnNdDVLKToqJyhfeWEpWBGLt9rsE"

    # 解碼成 64 bytes
    secret = base58.b58decode(base58_key)
    print("🔐 Secret length:", len(secret))  # 應為 64

    # 還原 Keypair 並印出公鑰
    kp = Keypair.from_bytes(secret)
    print("✅ Public key:", kp.pubkey())

except Exception as e:
    print("❌ Error occurred:", e)
