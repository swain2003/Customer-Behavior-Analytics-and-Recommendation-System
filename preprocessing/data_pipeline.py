from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class PipelineConfig:
    n_records: int = 120_000
    random_seed: int = 42


def generate_synthetic_transactions(config: PipelineConfig = PipelineConfig()) -> pd.DataFrame:
    """Generate synthetic 100k+ transaction records for customer analytics."""
    rng = np.random.default_rng(config.random_seed)
    n = config.n_records

    customer_ids = rng.integers(1, 12_001, size=n)
    dates = pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 730, size=n), unit="D")
    categories = rng.choice(
        ["Electronics", "Grocery", "Fashion", "Home", "Beauty", "Sports"],
        size=n,
        p=[0.18, 0.27, 0.2, 0.15, 0.1, 0.1],
    )

    df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "transaction_id": [f"TXN{1000000 + i}" for i in range(n)],
            "product_category": categories,
            "purchase_amount": np.round(rng.gamma(shape=2.4, scale=28, size=n), 2),
            "purchase_date": dates,
            "payment_method": rng.choice(["Card", "UPI", "Wallet", "Cash"], size=n),
            "city": rng.choice(["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai"], size=n),
            "gender": rng.choice(["Male", "Female", "Other"], size=n, p=[0.48, 0.49, 0.03]),
            "age": rng.integers(18, 71, size=n),
            "quantity": rng.integers(1, 6, size=n),
        }
    )

    tx_counts = df.groupby("customer_id")["transaction_id"].transform("count")
    max_date = df["purchase_date"].max()
    latest_purchase = df.groupby("customer_id")["purchase_date"].transform("max")
    df["frequency"] = tx_counts
    df["recency"] = (max_date - latest_purchase).dt.days

    missing_idx = rng.choice(df.index, size=max(1, n // 250), replace=False)
    df.loc[missing_idx[: len(missing_idx) // 2], "city"] = np.nan
    df.loc[missing_idx[len(missing_idx) // 2 :], "purchase_amount"] = np.nan

    return df


def preprocess_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset and create additional analytical features."""
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates(subset="transaction_id", keep="first")

    cleaned["purchase_amount"] = cleaned["purchase_amount"].fillna(cleaned["purchase_amount"].median())
    cleaned["city"] = cleaned["city"].fillna(cleaned["city"].mode().iloc[0])
    cleaned["purchase_date"] = pd.to_datetime(cleaned["purchase_date"])

    cleaned["revenue"] = cleaned["purchase_amount"] * cleaned["quantity"]
    cleaned["month"] = cleaned["purchase_date"].dt.to_period("M").astype(str)
    cleaned["age_group"] = pd.cut(
        cleaned["age"], bins=[17, 24, 34, 44, 54, 70], labels=["18-24", "25-34", "35-44", "45-54", "55-70"]
    )

    return cleaned


def export_pipeline_outputs(raw_df: pd.DataFrame, processed_df: pd.DataFrame, output_dir: str | Path = "data") -> None:
    """Export raw/processed datasets and BI-compatible monthly rollups."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    raw_df.to_csv(out / "transactions_raw.csv", index=False)
    processed_df.to_csv(out / "transactions_processed.csv", index=False)

    monthly = processed_df.groupby(["month", "product_category"], as_index=False)["revenue"].sum()
    monthly.to_csv(out / "bi_monthly_sales_export.csv", index=False)
