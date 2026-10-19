
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


FEATURES = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_7",
    "rolling_14",
    "day_of_week",
    "month",
]


def prepare_daily_series(sales_df):
    required_columns = {"date", "units_sold"}
    missing_columns = required_columns - set(sales_df.columns)

    if missing_columns:
        raise ValueError(
            f"Sales data is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if sales_df.empty:
        raise ValueError("Sales dataset is empty.")

    df = sales_df[["date", "units_sold"]].copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )

    df = df.dropna(subset=["date", "units_sold"])

    if df.empty:
        raise ValueError(
            "No valid date and units_sold records were found."
        )

    # Aggregate all product sales into a daily time series.
    daily = (
        df.groupby("date")["units_sold"]
        .sum()
        .sort_index()
    )

    # Ensure a consistent daily calendar.
    calendar = pd.date_range(
        start=daily.index.min(),
        end=daily.index.max(),
        freq="D",
    )

    daily = daily.reindex(calendar, fill_value=0)
    daily.index.name = "date"

    return daily.astype(float)


def create_features(series):
    df = pd.DataFrame({"target": series})

    df["lag_1"] = df["target"].shift(1)
    df["lag_7"] = df["target"].shift(7)
    df["lag_14"] = df["target"].shift(14)

    df["rolling_7"] = (
        df["target"].shift(1).rolling(window=7).mean()
    )

    df["rolling_14"] = (
        df["target"].shift(1).rolling(window=14).mean()
    )

    df["day_of_week"] = df.index.dayofweek
    df["month"] = df.index.month

    return df.dropna()


def forecast_sales(sales_df, horizon=14):
    if not isinstance(horizon, int) or isinstance(horizon, bool):
        raise ValueError("Forecast horizon must be an integer.")

    if horizon < 1 or horizon > 365:
        raise ValueError(
            "Forecast horizon must be between 1 and 365 days."
        )

    series = prepare_daily_series(sales_df)

    if len(series) < 35:
        raise ValueError(
            "At least 35 calendar days of sales history are required. "
            "Select All Products or use a longer historical period."
        )

    features = create_features(series)

    if len(features) < 20:
        raise ValueError(
            "Not enough observations to train the forecasting model."
        )

    # Chronological split: preserve time order during evaluation.
    split = int(len(features) * 0.80)

    train = features.iloc[:split]
    test = features.iloc[split:]

    if train.empty or test.empty:
        raise ValueError(
            "Not enough observations for chronological model evaluation."
        )

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=10,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(train[FEATURES], train["target"])

    predictions = np.maximum(
        0,
        model.predict(test[FEATURES]),
    )

    mae = mean_absolute_error(
        test["target"],
        predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(test["target"], predictions)
    )

    # Retrain using all available historical observations.
    final_model = RandomForestRegressor(
        n_estimators=150,
        max_depth=10,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    final_model.fit(
        features[FEATURES],
        features["target"],
    )

    history = series.copy()
    future_rows = []

    # Recursive multi-step forecasting.
    for _ in range(horizon):
        next_date = history.index[-1] + pd.Timedelta("1 day")

        row = pd.DataFrame(
            [{
                "lag_1": history.iloc[-1],
                "lag_7": history.iloc[-7],
                "lag_14": history.iloc[-14],
                "rolling_7": history.iloc[-7:].mean(),
                "rolling_14": history.iloc[-14:].mean(),
                "day_of_week": next_date.dayofweek,
                "month": next_date.month,
            }],
            columns=FEATURES,
        )

        estimate = max(
            0.0,
            float(final_model.predict(row)[0]),
        )

        future_rows.append({
            "date": next_date,
            "forecast_units": round(estimate, 2),
        })

        # Add the prediction to history for the next forecast step.
        history.loc[next_date] = estimate

    forecast_df = pd.DataFrame(future_rows)

    # Compatible with Pandas versions that do not support
    # Series.reset_index(names="date").
    history_df = (
        series.rename("units_sold")
        .rename_axis("date")
        .reset_index()
    )

    return {
        "forecast": forecast_df,
        "history": history_df,
        "mae": float(mae),
        "rmse": float(rmse),
    }
