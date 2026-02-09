import re
import pandas as pd
from sqlalchemy.engine import Engine
from utils.logger import get_logger 

logger = get_logger(__name__)


def _clean_table_name(name: str) -> str:
    """
    Clean table name to be SQL-safe
    """
    return re.sub(r"[^\w]+", "_", name.lower().strip())


def ingest_db(
    df: pd.DataFrame,
    table_name: str,
    engine: Engine,
) -> None:
    """
    Append DataFrame data into PostgreSQL table.
    Creates table automatically if it does not exist.
    """

    table_name = _clean_table_name(table_name)

    print(f"[INFO] Starting ingest into table '{table_name}' with {len(df)} rows")

    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=10_000,
            method="multi",
        )

        message = f"Appended {len(df)} rows into '{table_name}'"
        print(f"[SUCCESS] {message}")
        logger.info(message)

    except Exception as e:
        error_message = f"Failed loading data into table '{table_name}'"
        print(f"[ERROR] {error_message}: {e}")
        logger.exception(error_message)
        raise
