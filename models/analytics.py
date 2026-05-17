from __future__ import annotations

import pandas as pd


def calculate_clv(df: pd.DataFrame) -> pd.DataFrame:
    customer_value = df.groupby("customer_id", as_index=False).agg(
        total_revenue=("revenue", "sum"),
        transactions=("transaction_id", "count"),
        avg_purchase=("purchase_amount", "mean"),
    )
    customer_value["clv"] = customer_value["avg_purchase"] * customer_value["transactions"] * 1.3
    return customer_value.sort_values("clv", ascending=False)


def revenue_trend(df: pd.DataFrame) -> pd.DataFrame:
    trend = df.groupby("month", as_index=False)["revenue"].sum()
    return trend.sort_values("month")


def product_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("product_category", as_index=False)
        .agg(category_revenue=("revenue", "sum"), transactions=("transaction_id", "count"))
        .sort_values("category_revenue", ascending=False)
    )


def repeat_customer_analysis(df: pd.DataFrame) -> dict:
    tx = df.groupby("customer_id")["transaction_id"].count()
    repeat_customers = int((tx > 1).sum())
    total_customers = int(tx.size)
    repeat_rate = repeat_customers / total_customers if total_customers else 0
    return {
        "repeat_customers": repeat_customers,
        "total_customers": total_customers,
        "repeat_rate": round(repeat_rate, 4),
    }


def purchase_frequency_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("customer_id", as_index=False)["frequency"].max().sort_values("frequency", ascending=False)


def customer_retention_insights(df: pd.DataFrame) -> pd.DataFrame:
    customer_months = df.groupby("customer_id")["month"].nunique().rename("active_months")
    return customer_months.reset_index().sort_values("active_months", ascending=False)


def segment_wise_revenue_tracking(df: pd.DataFrame) -> pd.DataFrame:
    if "rfm_segment" not in df.columns:
        return pd.DataFrame(columns=["rfm_segment", "revenue"])
    return df.groupby("rfm_segment", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)


def top_customers_dashboard(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("customer_id", as_index=False)
        .agg(total_revenue=("revenue", "sum"), transactions=("transaction_id", "count"))
        .sort_values("total_revenue", ascending=False)
        .head(top_n)
    )
