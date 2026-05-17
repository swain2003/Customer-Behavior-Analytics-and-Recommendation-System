from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from models.analytics import calculate_clv, top_customers_dashboard
from recommendation.engine import popularity_based_recommendations, segment_based_recommendations
from visualizations.plots import category_heatmap, monthly_revenue_chart, segment_distribution_chart


DATA_PATH = Path("data/transactions_enriched.csv")


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        st.error("Run `python main.py` first to generate processed datasets.")
        st.stop()
    return pd.read_csv(DATA_PATH, parse_dates=["purchase_date"])


def render_kpis(df: pd.DataFrame) -> None:
    total_revenue = float(df["revenue"].sum())
    total_customers = int(df["customer_id"].nunique())
    avg_order = float(df["revenue"].mean())

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col2.metric("Unique Customers", f"{total_customers:,}")
    col3.metric("Average Order Value", f"₹{avg_order:,.2f}")


def main() -> None:
    st.set_page_config(page_title="Customer Behavior Analytics", layout="wide")
    st.title("Customer Behavior Analytics & Recommendation Dashboard")

    df = load_data()

    city_filter = st.sidebar.multiselect("Filter by City", sorted(df["city"].unique()), default=[])
    category_filter = st.sidebar.multiselect("Filter by Category", sorted(df["product_category"].unique()), default=[])
    customer_id = st.sidebar.number_input("Customer ID", min_value=1, max_value=int(df["customer_id"].max()), value=1)

    if city_filter:
        df = df[df["city"].isin(city_filter)]
    if category_filter:
        df = df[df["product_category"].isin(category_filter)]

    render_kpis(df)

    clv = calculate_clv(df)
    st.plotly_chart(monthly_revenue_chart(df), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(segment_distribution_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(clv.head(20), x="customer_id", y="clv", title="Top 20 CLV Customers"), use_container_width=True)

    st.plotly_chart(category_heatmap(df), use_container_width=True)

    st.subheader("Top Customers")
    st.dataframe(top_customers_dashboard(df), use_container_width=True)

    st.subheader("Personalized Recommendations")
    pop_recs = popularity_based_recommendations(df, int(customer_id))
    seg_recs = segment_based_recommendations(df, int(customer_id))
    st.write("Popularity-based:", pop_recs)
    st.write("Segment-based:", seg_recs)


if __name__ == "__main__":
    main()
