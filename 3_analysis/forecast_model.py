"""Time-series forecast: monthly sales projection with synthetic dates.

This script assigns synthetic transaction dates to the cleaned data (the
source has no date column), aggregates to monthly sales, and builds a
12-month forecast using linear regression with trend and monthly seasonality.

Limitation (stated clearly):
    The dates are synthetically assigned because the source dataset does not
    include order dates. The forecast demonstrates methodology only. Results
    indicate potential patterns but are NOT suitable for real business decisions.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

matplotlib.use("Agg")
warnings.filterwarnings("ignore", category=FutureWarning)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "3_analysis" / "outputs" / "superstore_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "3_analysis" / "outputs"


def create_synthetic_dates(df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Assign realistic synthetic dates to each transaction.

    Distribution logic (retail-typical):
      - 24 months: Jan 2022 to Dec 2023
      - Weekday weight 85% / weekend 15% (B2B skew)
      - Q4 months slightly heavier (holiday season proxy)
      - Random within each month
    """
    rng = np.random.default_rng(seed)
    n = len(df)
    n_rows = df.shape[0]

    # Monthly weights: slight Q4 bump
    monthly_weights = np.ones(24)
    for i in range(24):
        month = i % 12
        if month >= 9:  # Oct-Dec
            monthly_weights[i] = 1.5

    monthly_weights /= monthly_weights.sum()

    # Assign month indices (0-23) weighted
    month_indices = rng.choice(24, size=n_rows, p=monthly_weights)

    start_date = pd.Timestamp("2022-01-01")

    dates = []
    for mi in month_indices:
        month_start = start_date + pd.DateOffset(months=int(mi))
        month_end = month_start + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        days_in_month = month_end.day

        # Weekday bias: 85% chance of weekday
        while True:
            day = rng.integers(1, days_in_month + 1)
            candidate = month_start.replace(day=day)
            is_weekend = candidate.weekday() >= 5
            if is_weekend and rng.random() > 0.15:
                continue
            if not is_weekend and rng.random() > 0.85:
                continue
            dates.append(candidate)
            break

    df = df.copy()
    df["order_date"] = dates
    return df


def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales, profit, and transaction count by calendar month."""
    monthly = (
        df.set_index("order_date")
        .resample("ME")
        .agg(
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum"),
            transaction_lines=("Sales", "count"),
            avg_discount=("Discount", "mean"),
        )
        .reset_index()
    )
    monthly["margin_pct"] = (
        monthly["total_profit"] / monthly["total_sales"] * 100
    )
    return monthly


def engineer_features(monthly: pd.DataFrame) -> pd.DataFrame:
    """Create features for the regression model."""
    m = monthly.copy()
    m["month_num"] = range(len(m))
    m["month_of_year"] = m["order_date"].dt.month
    # One-hot encode month of year (seasonality)
    m = pd.get_dummies(m, columns=["month_of_year"], prefix="m", drop_first=True)
    return m


def build_forecast(
    monthly: pd.DataFrame,
    forecast_months: int = 12,
) -> tuple[pd.DataFrame, object, float, float]:
    """Train linear regression, forecast, return results and metrics."""
    feat_df = engineer_features(monthly)

    feature_cols = [c for c in feat_df.columns
                    if c.startswith("month_num") or c.startswith("m_")]

    X = feat_df[feature_cols].values
    y = feat_df["total_sales"].values

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)
    mae = mean_absolute_error(y, predictions)
    mape = mean_absolute_percentage_error(y, predictions)

    # Future periods
    last_date = monthly["order_date"].max()
    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=forecast_months,
        freq="ME",
    )

    future_feat = pd.DataFrame({"order_date": future_dates})
    future_feat["month_num"] = range(len(monthly), len(monthly) + forecast_months)
    future_feat["month_of_year"] = future_feat["order_date"].dt.month
    future_feat = pd.get_dummies(
        future_feat, columns=["month_of_year"], prefix="m", drop_first=True
    )

    # Ensure same columns as training
    for col in feature_cols:
        if col not in future_feat.columns:
            future_feat[col] = 0
    future_feat = future_feat[feature_cols]

    future_sales = model.predict(future_feat.values)

    forecast_df = pd.DataFrame(
        {
            "order_date": future_dates,
            "forecast_sales": future_sales,
        }
    )

    return forecast_df, model, mae, mape


def plot_forecast(
    monthly: pd.DataFrame,
    forecast_df: pd.DataFrame,
    save_path: Path,
) -> None:
    """Save forecast plot as PNG (for README and presentations)."""
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        monthly["order_date"],
        monthly["total_sales"] / 1000,
        marker="o",
        label="Historical (synthetic dates)",
        color="#1f77b4",
        linewidth=1.5,
    )

    ax.plot(
        forecast_df["order_date"],
        forecast_df["forecast_sales"] / 1000,
        marker="s",
        linestyle="--",
        label="Forecast (12 months)",
        color="#ff7f0e",
        linewidth=2,
    )

    ax.axvline(
        x=monthly["order_date"].max(),
        color="gray",
        linestyle=":",
        alpha=0.5,
        label="Forecast start",
    )

    ax.set_title("Monthly Sales — 12-Month Forecast", fontsize=14, fontweight="bold")
    ax.set_ylabel("Sales ($K)")
    ax.set_xlabel("")
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    fig.savefig(save_path, dpi=200)
    print(f"Saved forecast chart: {save_path.name}")

    # Also save a version in the deliverables folder for the slide deck
    slide_path = (
        PROJECT_ROOT / "5_deliverables" / "forecast_chart.png"
    )
    fig.savefig(slide_path, dpi=200)
    print(f"Saved forecast chart: {slide_path.name}")

    plt.close(fig)


def main() -> None:
    print("=" * 60)
    print("Sales Forecast Model")
    print("=" * 60)

    # Load data
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df):,} transaction rows")

    # Create synthetic dates
    df = create_synthetic_dates(df)
    date_range = f"{df['order_date'].min().date()} to {df['order_date'].max().date()}"
    print(f"Synthetic date range: {date_range}")

    # Export dataset with dates
    dated_path = OUTPUT_DIR / "superstore_with_dates.csv"
    df.to_csv(dated_path, index=False)
    print(f"Exported {dated_path.name}: {len(df)} rows with synthetic dates")

    # Aggregate to monthly
    monthly = aggregate_monthly(df)
    print(f"\nMonthly aggregation: {len(monthly)} months")
    print(f"Avg monthly sales: ${monthly['total_sales'].mean():>8,.0f}")
    print(f"Sales range: ${monthly['total_sales'].min():>8,.0f} - ${monthly['total_sales'].max():>8,.0f}")

    # Export monthly data
    monthly_path = OUTPUT_DIR / "20_monthly_sales_history.csv"
    monthly.to_csv(monthly_path, index=False)
    print(f"Exported {monthly_path.name}: {len(monthly)} rows")

    # Build forecast
    forecast_df, model, mae, mape = build_forecast(monthly, forecast_months=12)

    print(f"\n--- Model Performance ---")
    print(f"Mean Absolute Error:  ${mae:>8,.0f}")
    print(f"MAPE:                 {mape * 100:.1f}%")

    print(f"\n--- 12-Month Forecast ---")
    print(f"{'Month':<20} {'Forecast Sales':>15}")
    print("-" * 35)
    for _, row in forecast_df.iterrows():
        print(f"{row['order_date'].strftime('%b %Y'):<20} ${row['forecast_sales']:>10,.0f}")

    forecast_total = forecast_df["forecast_sales"].sum()
    historical_last_12 = monthly.tail(12)["total_sales"].sum()
    historical_yearly = monthly["total_sales"].sum()
    print(f"\nForecast annual total:     ${forecast_total:>10,.0f}")
    print(f"Last 12 months historical: ${historical_last_12:>10,.0f}")
    print(f"All 24 months historical:  ${historical_yearly:>10,.0f}")
    print(f"Projected vs last 12-mo:   {((forecast_total / historical_last_12) - 1) * 100:+.1f}%")

    # Export forecast
    forecast_path = OUTPUT_DIR / "21_forecast_12months.csv"
    forecast_df.to_csv(forecast_path, index=False)
    print(f"Exported {forecast_path.name}: {len(forecast_df)} rows")

    # Save chart
    chart_path = OUTPUT_DIR / "22_forecast_chart.png"
    plot_forecast(monthly, forecast_df, chart_path)

    print("\n" + "=" * 60)
    print("NOTE: Dates are synthetically assigned. The source dataset")
    print("has no order date column. This forecast demonstrates methodology")
    print("and should not be used for actual business planning.")
    print("=" * 60)


if __name__ == "__main__":
    main()
