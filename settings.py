from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
DB_PATH = DATA_DIR / "market_telemetry.db"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# CoinGecko Public API (No API key required)
API_URL = "https://coingecko.com"
ASSETS = ["bitcoin", "ethereum", "solana", "ripple", "cardano"]
CURRENCIES = ["usd", "zar"]
