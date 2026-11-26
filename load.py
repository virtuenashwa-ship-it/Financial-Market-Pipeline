import sqlite3
import logging
import pandas as pd
from config.settings import DB_PATH

logger = logging.getLogger(__name__)

def load_to_sqlite(df: pd.DataFrame):
    """Persist cleaned market metrics into SQLite and update analytical summary view."""
    with sqlite3.connect(DB_PATH) as conn:
        # 1. Append historical readings
        df_to_save = df.copy()
        df_to_save["extracted_at"] = df_to_save["extracted_at"].astype(str)
        df_to_save.to_sql("market_prices_history", conn, if_exists="append", index=False)

        # 2. Build SQL Summary View (Average prices & max volatility per asset)
        conn.execute("""
            CREATE VIEW IF NOT EXISTS vw_asset_performance AS
            SELECT
                asset,
                COUNT(*) AS snapshots_recorded,
                ROUND(AVG(price_usd), 2) AS avg_price_usd,
                ROUND(AVG(price_zar), 2) AS avg_price_zar,
                ROUND(AVG(implied_usd_zar_rate), 2) AS avg_usd_zar_rate,
                ROUND(MAX(change_24h_pct), 2) AS peak_24h_gain_pct,
                ROUND(MIN(change_24h_pct), 2) AS worst_24h_drop_pct
            FROM market_prices_history
            GROUP BY asset
            ORDER BY avg_volume_usd DESC;
        """.replace("ORDER BY avg_volume_usd DESC", "ORDER BY avg_price_usd DESC"))

    logger.info(f"Loaded {len(df)} rows into SQLite ({DB_PATH.name}) and updated SQL view")
