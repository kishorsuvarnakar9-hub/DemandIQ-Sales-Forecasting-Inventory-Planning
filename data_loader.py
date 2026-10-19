
from pathlib import Path

import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"


def load_sales_data():
    file_path = DATA_DIR / "enterprise_revenue_dataset.xlsx"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Sales Excel file not found: {file_path}"
        )

    excel_file = pd.ExcelFile(file_path)

    required = [
        "order_date",
        "product_id",
        "units_sold",
        "revenue",
    ]

    df = None

    # Find the worksheet containing the required sales columns
    for sheet_name in excel_file.sheet_names:
        temp = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
        )

        temp.columns = temp.columns.astype(str).str.strip()

        if all(column in temp.columns for column in required):
            df = temp.copy()
            print(f"Sales worksheet selected: {sheet_name}")
            break

    if df is None:
        raise ValueError(
            "Required sales columns were not found. "
            f"Worksheets: {excel_file.sheet_names}"
        )

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce",
    )

    df["units_sold"] = pd.to_numeric(
        df["units_sold"],
        errors="coerce",
    ).fillna(0).clip(lower=0)

    df["revenue"] = pd.to_numeric(
        df["revenue"],
        errors="coerce",
    ).fillna(0).clip(lower=0)

    df["product_id"] = (
        df["product_id"].astype("string").str.strip()
    )

    df = df.dropna(
        subset=["order_date", "product_id"]
    )

    df = df[df["product_id"] != ""].copy()

    # The sales dataset has no product_name column
    if "product_name" not in df.columns:
        df["product_name"] = df["product_id"]

    df["product_name"] = (
        df["product_name"]
        .fillna(df["product_id"])
        .astype(str)
    )

    daily = (
        df.groupby(
            [
                pd.Grouper(key="order_date", freq="D"),
                "product_id",
                "product_name",
            ],
            as_index=False,
        )
        .agg(
            units_sold=("units_sold", "sum"),
            revenue=("revenue", "sum"),
        )
        .rename(columns={"order_date": "date"})
    )

    return daily.sort_values("date").reset_index(drop=True)


def load_inventory_data():
    # Correct filename and Excel reader
    file_path = DATA_DIR / "inventory_planning_10000.xlsx"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Inventory Excel file not found: {file_path}\n"
            "Check the filename and extension inside data/raw."
        )

    # Automatically find the worksheet with inventory columns
    excel_file = pd.ExcelFile(file_path)

    required = [
        "date",
        "product_id",
        "warehouse",
        "current_stock",
        "reorder_point",
        "lead_time_days",
        "supplier_rating",
    ]

    df = None

    for sheet_name in excel_file.sheet_names:
        temp = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
        )

        temp.columns = temp.columns.astype(str).str.strip()

        if all(column in temp.columns for column in required):
            df = temp.copy()
            print(f"Inventory worksheet selected: {sheet_name}")
            break

    if df is None:
        raise ValueError(
            "Required inventory columns were not found. "
            f"Worksheets: {excel_file.sheet_names}"
        )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    df["product_id"] = (
        df["product_id"].astype("string").str.strip()
    )

    df["warehouse"] = (
        df["warehouse"].astype("string").str.strip()
    )

    numeric_columns = [
        "current_stock",
        "reorder_point",
        "lead_time_days",
        "supplier_rating",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    df = df.dropna(
        subset=[
            "date",
            "product_id",
            "warehouse",
            "current_stock",
            "reorder_point",
            "lead_time_days",
        ]
    )

    df = df[
        (df["product_id"] != "")
        & (df["warehouse"] != "")
    ].copy()

    # Keep the latest record for each product and warehouse
    df = (
        df.sort_values("date")
        .drop_duplicates(
            subset=["product_id", "warehouse"],
            keep="last",
        )
        .copy()
    )

    df["current_stock"] = df["current_stock"].clip(lower=0)
    df["reorder_point"] = df["reorder_point"].clip(lower=0)
    df["lead_time_days"] = df["lead_time_days"].clip(lower=0)
    df["supplier_rating"] = df["supplier_rating"].clip(0, 5)

    df["stock_status"] = np.where(
        df["current_stock"] <= df["reorder_point"],
        "Reorder",
        "Healthy",
    )

    return df.reset_index(drop=True)
