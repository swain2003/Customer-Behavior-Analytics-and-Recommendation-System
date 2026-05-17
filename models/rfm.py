from __future__ import annotations

import pandas as pd


SEGMENT_MAP = {
    "555": "High Value Customers",
    "554": "Loyal Customers",
    "455": "Loyal Customers",
    "355": "Potential Customers",
    "155": "At Risk Customers",
    "111": "Lost Customers",
}


def build_rfm_table(df: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = df["purchase_date"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("customer_id", as_index=False).agg(
        Recency=("purchase_date", lambda x: (snapshot_date - x.max()).days),
        Frequency=("transaction_id", "count"),
        Monetary=("revenue", "sum"),
    )

    rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["RFM_Score"] = rfm[["R_Score", "F_Score", "M_Score"]].astype(str).agg("".join, axis=1)
    rfm["rfm_segment"] = rfm["RFM_Score"].map(SEGMENT_MAP).fillna("Potential Customers")
    return rfm
