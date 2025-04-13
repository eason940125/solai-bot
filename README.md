# 🚀 SolAI Sniper Bot（實戰正式版）

SolAI Sniper Bot 是一套部署在 Solana 鏈上的智能狙擊機器人，整合 AI 倉位管理、Jupiter Swap 路徑、Pump.fun 掃鏈與自動實單功能，可在 Telegram 接收通知並實現完全自動交易。

---

## ✅ 支援功能模組

| 模組 | 功能說明 |
|------|----------|
| `auto_chain_sniper.py` | ✅ 每分鐘掃鏈 Pump.fun，新幣自動下單 + Telegram 通知 |
| `auto_sniper_loop.py` | ✅ 固定幣種多個掃描 + 狙擊（SNIPER_MINT 設定） |
| `auto_sniper_trader.py` | ✅ 提供 `/snipe` HTTP 入口觸發交易 |
| `jupiter_trading.py` | ✅ Swap 路徑分析、真實交易下單整合 |
| `gmgn_trading.py` | ✅ 轉帳交易模組（測試或基礎下單用） |
| `ai_logic.py` | ✅ 根據 mint address 評估信心與倉位金額 |
| `main.py` | ✅ Telegram webhook 入口，管理 /start, /help 等指令 |

---

## ☁️ Render 部署教學

### 🪜 步驟：

1. 前往 [Render](https://render.com)
2. 建立一個「Background Worker」服務
3. 設定：
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `python auto_chain_sniper.py`

4. 設定以下 `.env` 環境變數（請在 Render > Environment 新增）：

```env
BOT_TOKEN=你的 Telegram Bot Token
CHAT_ID=你的 chat_id
PRIVATE_KEY=你的 base64 私鑰
WALLET_PUBLIC_KEY=你的 Solana 錢包地址
RPC_URL=https://mainnet.rpcpool.com
```

✅ **不需要 SNIPER_MINT，因為會自動掃鏈找新幣**

---

## 🧠 AI 倉位配置說明（ai_logic.py）

- 自動根據 mint address 評估信心分數（0~1）
- 決定對應下單金額：
  - 0.9↑ = 0.08 SOL
  - 0.8↑ = 0.05 SOL
  - 0.7↑ = 0.03 SOL
  - 其餘 = 0.02 SOL

---

## 🔐 注意事項

- ✅ 本專案為 **真實交易版本**，一啟動即會消耗 SOL
- ✅ 請務必使用乾淨/測試用錢包
- ❌ 請勿公開 `.env` 正式私鑰檔案

---

## 📦 推薦資料夾結構

```
solai-sniper-bot/
├── auto_chain_sniper.py       # ✅ 自動掃鏈主程式
├── auto_sniper_loop.py        # 固定幣種多重掃描
├── auto_sniper_trader.py      # 手動 HTTP 狙擊觸發
├── jupiter_trading.py         # Swap 池分析與發送交易
├── gmgn_trading.py            # 簡單轉帳交易工具
├── ai_logic.py                # AI 倉位評估模組
├── main.py                    # Telegram Bot webhook 入口
├── requirements.txt
├── .env.example               # ✅ 可分享的環境變數模板
└── README.md
```

---

## ✅ 啟動指令（本地測試）

```bash
pip install -r requirements.txt
python auto_chain_sniper.py
```

---

## 🧠 功能持續更新中…

- 支援社群情緒判斷
- 自動止盈止損
- 多錢包策略
- 策略週報 / 回測績效報告

歡迎貢獻改進，或私訊作者獲得 VIP 強化版 🚀
