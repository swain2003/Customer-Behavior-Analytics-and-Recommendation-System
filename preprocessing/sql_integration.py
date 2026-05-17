from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sqlalchemy import create_engine


@dataclass
class SQLConfig:
    connection_uri: str = "mysql+pymysql://root:password@localhost:3306/customer_behavior"
    table_name: str = "transactions_processed"


def write_dataframe_to_sql(df: pd.DataFrame, config: SQLConfig) -> None:
    """Persist processed customer transactions into MySQL."""
    engine = create_engine(config.connection_uri)
    df.to_sql(config.table_name, engine, if_exists="replace", index=False)
