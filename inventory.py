
import numpy as np
import pandas as pd


def make_inventory_plan(inventory_df, sales_df):
    inv = inventory_df.copy()

    if sales_df.empty:
        inv["estimated_daily_demand"] = np.nan
    else:
        # Average observed daily demand per product.
        demand = (
            sales_df.groupby("product_id")
            .agg(
                estimated_daily_demand=("units_sold", "mean")
            )
            .reset_index()
        )

        inv = inv.merge(
            demand,
            on="product_id",
            how="left"
        )

    # If product IDs do not match, derive a transparent fallback
    # from reorder point and lead time. This is NOT an ML forecast.
    fallback = (
        inv["reorder_point"] /
        (inv["lead_time_days"] + 1).clip(lower=1)
    ).clip(lower=1)

    inv["estimated_daily_demand"] = (
        inv["estimated_daily_demand"]
        .fillna(fallback)
        .clip(lower=0)
    )

    # Simple target stock: lead-time demand plus the existing buffer
    # represented by the difference between reorder point and lead-time demand.
    lead_time_demand = (
        inv["estimated_daily_demand"] * inv["lead_time_days"]
    )

    buffer_stock = np.maximum(
        0,
        inv["reorder_point"] - lead_time_demand
    )

    target_stock = (
        lead_time_demand
        + buffer_stock
        + inv["estimated_daily_demand"] * 7
    )

    inv["suggested_order_qty"] = np.maximum(
        0,
        np.ceil(target_stock - inv["current_stock"])
    ).astype(int)

    inv["stock_status"] = np.where(
        inv["current_stock"] <= inv["reorder_point"],
        "Reorder",
        "Healthy"
    )

    inv["estimated_daily_demand"] = (
        inv["estimated_daily_demand"].round(2)
    )

    return inv
