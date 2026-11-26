# Financial Market Data Pipeline

An end-to-end data pipeline that extracts live USD and ZAR market data for major digital assets from the CoinGecko API, calculates implied USD/ZAR exchange rates and 24-hour volatility flags, and stores structured records and analytical SQL views in **SQLite** using **Python**, **Pandas**, and **Requests**.

## Architecture Overview

This pipeline separates raw ingestion from transformation and SQL reporting across modular stages:

1. **Extract (`src/extract.py`):** Fetches live USD and ZAR prices, 24-hour percentage changes, and 24-hour volumes for target assets (`bitcoin`, `ethereum`, `solana`, `ripple`, `cardano`) using exponential backoff retries (`tenacity`) and saves timestamped raw JSON snapshots under `data/raw/`.
2. **Transform (`src/transform.py`):** Loads raw JSON snapshots into a **Pandas** DataFrame, computes the implied USD/ZAR exchange rate (`price_zar / price_usd`), flags high-volatility movers (`abs(change_24h) >= 5.0%`), and sorts assets by 24-hour performance.
3. **Load & Aggregate (`src/load.py`):** Appends cleaned records into the `market_prices_history` table in **SQLite** (`data/market_telemetry.db`) and maintains the `vw_asset_performance` SQL view summarizing average prices, average implied USD/ZAR rates, and peak/worst 24-hour swings per asset.
4. **Orchestration (`src/pipeline.py`):** Runs extraction, transformation, terminal table output, and database loading in sequence with console and file logging (`market_pipeline.log`).

## Project Structure

```text
financial-market-pipeline/
├── config/
│   └── settings.py          # Directory paths, API endpoint, target assets, and currencies
├── src/
│   ├── extract.py           # Market API ingestion with retry/backoff and raw JSON archiving
│   ├── transform.py         # JSON flattening, implied USD/ZAR rate, and volatility flags
│   ├── load.py              # SQLite persistence and vw_asset_performance SQL view
│   └── pipeline.py          # Pipeline runner with console table output and logging
├── requirements.txt         # Project dependencies
├── .gitignore               # Excludes local databases, logs, cache, and raw data files
└── README.md                # Project documentation
