"""What-if scenario model: how would profit change if we capped discounts?

Approach
---------
For each transaction line where the current discount exceeds the scenario cap:
  1. Implied base price = Sales / (1 - Discount)   — price before any discount
  2. Cost              = Sales - Profit             — inferred total cost
  3. New Sales         = Implied base price * (1 - cap)
  4. New Profit        = New Sales - Cost
  5. Delta             = New Profit - Profit

Key assumption: the same quantity is sold at the lower discount (optimistic).
This gives an upper-bound estimate of profit improvement.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "3_analysis" / "outputs" / "superstore_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "3_analysis" / "outputs"


def run_scenarios() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    # Infer cost per line (total, not per-unit)
    df["implied_base_sales"] = df["Sales"] / (1 - df["Discount"])
    df["cost"] = df["Sales"] - df["Profit"]

    scenarios = {
        "A - Cap at 30%": 0.30,
        "B - Cap at 20%": 0.20,
        "C - Zero discount": 0.00,
    }

    results = []
    for scenario_name, cap in scenarios.items():
        cap_mask = df["Discount"] > cap
        n_affected = cap_mask.sum()

        new_sales = df["Sales"].copy()
        new_profit = df["Profit"].copy()

        # Recalculate for affected rows
        new_sales.loc[cap_mask] = (
            df.loc[cap_mask, "implied_base_sales"] * (1 - cap)
        )
        new_profit.loc[cap_mask] = new_sales.loc[cap_mask] - df.loc[cap_mask, "cost"]

        delta_profit = new_profit.sum() - df["Profit"].sum()
        new_margin = new_profit.sum() / new_sales.sum() * 100

        results.append(
            {
                "scenario": scenario_name,
                "cap": cap,
                "total_sales": round(new_sales.sum(), 2),
                "total_profit": round(new_profit.sum(), 2),
                "margin_pct": round(new_margin, 2),
                "delta_sales": round(new_sales.sum() - df["Sales"].sum(), 2),
                "delta_profit": round(delta_profit, 2),
                "rows_affected": int(n_affected),
                "pct_rows_affected": round(n_affected / len(df) * 100, 1),
            }
        )

    result_df = pd.DataFrame(results)
    return result_df


def main() -> None:
    result_df = run_scenarios()

    print("What-If Scenario Results")
    print("=" * 70)
    print(
        f"{'Scenario':<25} {'Sales':>12} {'Profit':>12} {'Margin':>8} {'Chg Profit':>10} {'Rows':>6}"
    )
    print("-" * 70)
    for _, row in result_df.iterrows():
        print(
            f"{row['scenario']:<25} "
            f"${row['total_sales']:>9,.0f} "
            f"${row['total_profit']:>9,.0f} "
            f"{row['margin_pct']:>7.2f}% "
            f"${row['delta_profit']:>+7,.0f} "
            f"{row['rows_affected']:>5}"
        )
    print("=" * 70)

    export_path = OUTPUT_DIR / "16_scenario_comparison.csv"
    result_df.to_csv(export_path, index=False)
    print(f"Exported {export_path.name}: {len(result_df)} rows")

    affected_path = OUTPUT_DIR / "17_affected_rows_for_cap_20.csv"
    df = pd.read_csv(DATA_PATH)
    df["implied_base_sales"] = df["Sales"] / (1 - df["Discount"])
    df["cost"] = df["Sales"] - df["Profit"]
    affected = df[df["Discount"] > 0.20].copy()
    affected["capped_sales"] = affected["implied_base_sales"] * (1 - 0.20)
    affected["capped_profit"] = affected["capped_sales"] - affected["cost"]
    affected["profit_delta"] = affected["capped_profit"] - affected["Profit"]
    affected.to_csv(affected_path, index=False)
    print(f"Exported {affected_path.name}: {len(affected)} rows")


if __name__ == "__main__":
    main()
