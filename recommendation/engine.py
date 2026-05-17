from __future__ import annotations

import pandas as pd


def popularity_based_recommendations(df: pd.DataFrame, customer_id: int, top_n: int = 5) -> list[str]:
    customer_categories = set(df.loc[df["customer_id"] == customer_id, "product_category"].tolist())
    ranked = (
        df.groupby("product_category", as_index=False)
        .agg(revenue=("revenue", "sum"), demand=("quantity", "sum"))
        .sort_values(["revenue", "demand"], ascending=False)
    )
    recs = [c for c in ranked["product_category"].tolist() if c not in customer_categories]
    return recs[:top_n]


def segment_based_recommendations(df: pd.DataFrame, customer_id: int, top_n: int = 5) -> list[str]:
    if "rfm_segment" not in df.columns:
        return popularity_based_recommendations(df, customer_id, top_n)

    segment_series = df.loc[df["customer_id"] == customer_id, "rfm_segment"]
    if segment_series.empty:
        return popularity_based_recommendations(df, customer_id, top_n)

    segment = segment_series.iloc[0]
    segment_df = df[df["rfm_segment"] == segment]
    ranked = (
        segment_df.groupby("product_category", as_index=False)
        .agg(transactions=("transaction_id", "count"), revenue=("revenue", "sum"))
        .sort_values(["transactions", "revenue"], ascending=False)
    )
    return ranked["product_category"].head(top_n).tolist()
