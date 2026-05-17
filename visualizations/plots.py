from __future__ import annotations

import plotly.express as px
import pandas as pd


def monthly_revenue_chart(df: pd.DataFrame):
    monthly = df.groupby("month", as_index=False)["revenue"].sum().sort_values("month")
    return px.line(monthly, x="month", y="revenue", markers=True, title="Monthly Revenue Trend")


def segment_distribution_chart(rfm_df: pd.DataFrame):
    seg = rfm_df["rfm_segment"].value_counts().reset_index()
    seg.columns = ["segment", "customers"]
    return px.pie(seg, names="segment", values="customers", title="Customer Segment Distribution")


def category_heatmap(df: pd.DataFrame):
    pivot = df.pivot_table(index="city", columns="product_category", values="revenue", aggfunc="sum", fill_value=0)
    return px.imshow(pivot, title="City vs Category Revenue Heatmap", aspect="auto")
