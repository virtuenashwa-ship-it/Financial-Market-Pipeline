import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.extract import extract_and_save_raw
from src.transform import transform_market_data
from src.load import load_to_sqlite

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("market_pipeline.log")]
)
logger = logging.getLogger(__name__)

def run():
    logger.info("=== Starting Financial Market Data Pipeline ===")
    try:
        raw_file = extract_and_save_raw()
        df = transform_market_data(raw_file)
        print("\n--- Live Market Snapshot (Sorted by 24h Gain) ---")
        print(df[["asset", "price_usd", "price_zar", "implied_usd_zar_rate", "change_24h_pct", "volatility_status"]].to_string(index=False))
        print("-------------------------------------------------\n")
        load_to_sqlite(df)
        logger.info("=== Pipeline Finished Successfully ===")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")

if __name__ == "__main__":
    run()
