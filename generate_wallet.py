from solders.keypair import Keypair
import base58

# 產生新的 Solana 金鑰對
kp = Keypair()

# 將私鑰轉為 base58 格式（方便儲存）
secret_key_base58 = base58.b58encode(bytes(kp)).decode("utf-8")

# 顯示錢包資訊
print("✅ 私鑰 Base58：", secret_key_base58)
print("✅ 公鑰地址：", kp.pubkey())
