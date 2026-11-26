import json
import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

def transform_market_data(raw_file: Path) -> pd.DataFrame:
    """Flatten JSON payload, calculate implied USD/ZAR rate, and classify volatility."""
    with open(raw_file, "r") as f:
        payload = json.load(f)

    extracted_at = pd.to_datetime(payload["extracted_at"])
    records = []

    for asset, metrics in payload["data"].items():
        price_usd = float(metrics.get("usd", 0))
        price_zar = float(metrics.get("zar", 0))
        change_24h = float(metrics.get("usd_24h_change", 0))
        vol_24h_usd = float(metrics.get("usd_24h_vol", 0))

        # Derive implied USD/ZAR exchange rate from asset pricing
        implied_usd_zar = round(price_zar / price_usd, 4) if price_usd > 0 else 0.0

        # Flag high volatility (> 5% swing in 24h)
        volatility_flag = "HIGH" if abs(change_24h) >= 5.0 else "NORMAL"

        records.append({
            "asset": asset.capitalize(),
            "price_usd": round(price_usd, 2),
            "price_zar": round(price_zar, 2),
            "implied_usd_zar_rate": implied_usd_zar,
            "change_24h_pct": round(change_24h, 2),
            "volume_24h_usd": round(vol_24h_usd, 2),
            "volatility_status": volatility_flag,
            "extracted_at": extracted_at
        })

    df = pd.DataFrame(records)
    # Sort by highest 24h percentage mover
    df = df.sort_values(by="change_24h_pct", ascending=False).reset_index(drop=True)

    logger.info(f"Transformed {len(df)} market asset records")
    return df
