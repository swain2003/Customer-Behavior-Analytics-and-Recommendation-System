from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def prepare_clustering_features(rfm_df: pd.DataFrame) -> pd.DataFrame:
    return rfm_df[["Recency", "Frequency", "Monetary"]].copy()


def elbow_method(features: pd.DataFrame, max_k: int = 10) -> pd.DataFrame:
    scaler = StandardScaler()
    x = scaler.fit_transform(features)
    ks, inertias = [], []
    for k in range(2, max_k + 1):
        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        model.fit(x)
        ks.append(k)
        inertias.append(model.inertia_)
    return pd.DataFrame({"k": ks, "inertia": inertias})


def fit_kmeans(rfm_df: pd.DataFrame, n_clusters: int = 5) -> pd.DataFrame:
    scaler = StandardScaler()
    features = prepare_clustering_features(rfm_df)
    x = scaler.fit_transform(features)
    model = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    rfm_df = rfm_df.copy()
    rfm_df["cluster"] = model.fit_predict(x)
    return rfm_df


def save_cluster_plot(clustered_df: pd.DataFrame, output_path: str = "visualizations/cluster_scatter.png") -> None:
    plt.figure(figsize=(9, 6))
    scatter = plt.scatter(
        clustered_df["Recency"],
        clustered_df["Monetary"],
        c=clustered_df["cluster"],
        cmap="viridis",
        alpha=0.6,
    )
    plt.title("Customer Cluster Visualization")
    plt.xlabel("Recency")
    plt.ylabel("Monetary")
    plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()
