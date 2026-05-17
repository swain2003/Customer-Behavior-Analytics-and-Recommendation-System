from __future__ import annotations

import argparse

from models.analytics import calculate_clv
from models.clustering import elbow_method, fit_kmeans, save_cluster_plot
from models.rfm import build_rfm_table
from preprocessing.data_pipeline import PipelineConfig, export_pipeline_outputs, generate_synthetic_transactions, preprocess_transactions


def run_pipeline(rows: int = 120_000) -> None:
    raw_df = generate_synthetic_transactions(PipelineConfig(n_records=rows))
    processed_df = preprocess_transactions(raw_df)
    export_pipeline_outputs(raw_df, processed_df, output_dir="data")

    rfm_df = build_rfm_table(processed_df)
    clustered_rfm = fit_kmeans(rfm_df, n_clusters=5)
    elbow_df = elbow_method(rfm_df[["Recency", "Frequency", "Monetary"]], max_k=10)

    enriched = processed_df.merge(clustered_rfm[["customer_id", "rfm_segment", "cluster"]], on="customer_id", how="left")
    enriched.to_csv("data/transactions_enriched.csv", index=False)
    clustered_rfm.to_csv("data/rfm_segments.csv", index=False)
    elbow_df.to_csv("data/elbow_method.csv", index=False)
    calculate_clv(enriched).to_csv("data/customer_clv.csv", index=False)

    save_cluster_plot(clustered_rfm, output_path="visualizations/cluster_scatter.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Customer Behavior Analytics Pipeline")
    parser.add_argument("--rows", type=int, default=120_000, help="Number of synthetic transactions to generate")
    args = parser.parse_args()

    run_pipeline(rows=args.rows)
    print("Pipeline completed. Launch dashboard with: streamlit run dashboard/streamlit_app.py")


if __name__ == "__main__":
    main()
