import json
import logging
from datetime import datetime, timezone
from pathlib import Path
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import API_URL, ASSETS, CURRENCIES, RAW_DIR

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_market_prices() -> dict:
    """Fetch live asset prices in USD and ZAR with 24h change and volume."""
    params = {
        "ids": ",".join(ASSETS),
        "vs_currencies": ",".join(CURRENCIES),
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    response = requests.get(API_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json()

def extract_and_save_raw() -> Path:
    """Extract live market JSON and archive raw snapshot."""
    raw_data = fetch_market_prices()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_path = RAW_DIR / f"market_snapshot_{timestamp}.json"

    payload = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "data": raw_data
    }

    with open(file_path, "w") as f:
        json.dump(payload, f, indent=2)

    logger.info(f"Saved raw market snapshot -> {file_path.name}")
    return file_path
