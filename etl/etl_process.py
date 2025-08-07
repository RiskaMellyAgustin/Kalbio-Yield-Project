import pandas as pd
from django.db import connection
from datetime import datetime
import os
import logging
from yieldapp.models.merge import MergedYield

# Setup logging
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "etl_log.txt")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def fetch_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        cols = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=cols)


def run_etl():
    try:
        # Ambil semua data dari tabel-tabel terkait
        df_yield = fetch_query("SELECT * FROM yieldapp_operatoryielddata")
        df_batch = fetch_query("SELECT * FROM yieldapp_batchinfo")
        df_product = fetch_query("SELECT * FROM yieldapp_product")
        df_issue = fetch_query("SELECT * FROM yieldapp_issue")

        # Merge data
        merged = (
            df_yield.merge(
                df_batch, left_on="batch_id", right_on="id", suffixes=("", "_batch")
            )
            .merge(
                df_product,
                left_on="product_id",
                right_on="id",
                suffixes=("", "_product"),
            )
            .merge(
                df_issue,
                left_on="batch_id",
                right_on="batch_id",
                how="left",
                suffixes=("", "_issue"),
            )
        )

        # Hitung total output dan yield
        merged["total_output"] = (
            merged["formulation_output_pcs"]
            + merged["filling_output"]
            + merged["inspection_output"]
            + merged["assembly_output"]
            + merged["blistering_output"]
            + merged["packaging_output"]
            + merged["handover_output"]
        )

        merged["yield_percent"] = (
            merged["total_output"] / merged["theoritical_yield_pcs"]
        ) * 100

        # Hanya hapus baris yang ada NaN di kolom-kolom penting untuk insert
        merged = merged.dropna(
            subset=[
                "batch_id",
                "product_id",
                "formulation_output_pcs",
                "filling_output",
                "inspection_output",
                "assembly_output",
                "blistering_output",
                "packaging_output",
                "handover_output",
                "theoritical_yield_pcs",
                "total_output",
                "yield_percent",
            ]
        )

        for _, row in merged.iterrows():
            MergedYield.objects.create(
                batch_id=row["batch_id"],
                product_id=row["product_id"],
                formulation_output_pcs=row["formulation_output_pcs"],
                filling_output=row["filling_output"],
                inspection_output=row["inspection_output"],
                assembly_output=row["assembly_output"],
                blistering_output=row["blistering_output"],
                packaging_output=row["packaging_output"],
                handover_output=row["handover_output"],
                theoritical_yield_pcs=row["theoritical_yield_pcs"],
                total_output=row["total_output"],
                yield_percent=row["yield_percent"],
            )

        logging.info("ETL process completed successfully and data saved to DB.")
    except Exception as e:
        logging.error("ETL process failed: %s", str(e))
        raise e
