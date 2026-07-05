from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "3_analysis" / "outputs" / "superstore_cleaned.csv"


st.set_page_config(
    page_title="Sales Discount Strategy Analysis",
    page_icon="",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    numeric_columns = ["Sales", "Quantity", "Discount", "Profit"]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    if "Order Date" in data.columns:
        data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
    return data


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_percent(value: float) -> str:
    return f"{value:.1f}%"


def kpi_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
    }
    .kpi-card {
        border: 1px solid #d7dce2;
        border-radius: 8px;
        padding: 14px 16px;
        background: #ffffff;
        min-height: 92px;
    }
    .kpi-label {
        color: #5f6b7a;
        font-size: 0.86rem;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #111827;
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.2;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


df = load_data()

st.title("Sales Discount Strategy Analysis")
st.caption("Interactive view of regional, category, discount, and margin performance from the cleaned Superstore analytical snapshot.")

with st.sidebar:
    st.header("Filters")
    selected_regions = st.multiselect(
        "Region",
        sorted(df["Region"].dropna().unique()),
        default=sorted(df["Region"].dropna().unique()),
    )
    selected_categories = st.multiselect(
        "Category",
        sorted(df["Category"].dropna().unique()),
        default=sorted(df["Category"].dropna().unique()),
    )

    date_available = "Order Date" in df.columns and df["Order Date"].notna().any()
    if date_available:
        min_date = df["Order Date"].min().date()
        max_date = df["Order Date"].max().date()
        selected_dates = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    else:
        selected_dates = None
        st.info("Date range filtering is unavailable because the source data has no order date column.")


filtered = df[df["Region"].isin(selected_regions) & df["Category"].isin(selected_categories)].copy()

if date_available and selected_dates and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered = filtered[
        (filtered["Order Date"].dt.date >= start_date)
        & (filtered["Order Date"].dt.date <= end_date)
    ]

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
margin_pct = (total_profit / total_sales * 100) if total_sales else 0
transaction_lines = len(filtered)

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
with kpi_1:
    kpi_card("Total Sales", format_currency(total_sales))
with kpi_2:
    kpi_card("Total Profit", format_currency(total_profit))
with kpi_3:
    kpi_card("Margin %", format_percent(margin_pct))
with kpi_4:
    kpi_card("Transaction Lines", f"{transaction_lines:,}")

st.divider()

trend_col, category_col = st.columns((1.35, 1))

with trend_col:
    st.subheader("Sales Trend")
    if date_available:
        monthly_sales = (
            filtered.assign(month=filtered["Order Date"].dt.to_period("M").dt.to_timestamp())
            .groupby("month", as_index=False)["Sales"]
            .sum()
        )
        fig = px.line(monthly_sales, x="month", y="Sales", markers=True, labels={"month": "Month", "Sales": "Sales"})
        fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=360)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("A true sales trend cannot be charted because the current dataset has no date column.")

with category_col:
    st.subheader("Profit by Category")
    category_profit = (
        filtered.groupby("Category", as_index=False)
        .agg(total_profit=("Profit", "sum"), total_sales=("Sales", "sum"))
        .sort_values("total_profit", ascending=False)
    )
    fig = px.bar(
        category_profit,
        x="Category",
        y="total_profit",
        color="Category",
        labels={"total_profit": "Profit", "Category": "Category"},
    )
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=20, b=10), height=360)
    st.plotly_chart(fig, use_container_width=True)

scatter_col, table_col = st.columns((1.1, 1.25))

with scatter_col:
    st.subheader("Discount vs. Profit")
    fig = px.scatter(
        filtered,
        x="Discount",
        y="Profit",
        color="Category",
        hover_data=["Region", "State", "Sub-Category", "Sales", "Quantity"],
        labels={"Discount": "Discount Rate", "Profit": "Profit"},
    )
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=420)
    st.plotly_chart(fig, use_container_width=True)

with table_col:
    st.subheader("Top and Bottom Sub-Categories")
    st.caption("Sub-category is the most granular product field available in the source data.")
    product_view = (
        filtered.groupby(["Category", "Sub-Category"], as_index=False)
        .agg(total_sales=("Sales", "sum"), total_profit=("Profit", "sum"), transaction_lines=("Sales", "count"))
    )
    product_view["margin_pct"] = product_view["total_profit"] / product_view["total_sales"] * 100
    product_view = product_view.sort_values("total_profit", ascending=False)

    top_10 = product_view.head(10).assign(rank_group="Top 10")
    bottom_10 = product_view.tail(10).sort_values("total_profit").assign(rank_group="Bottom 10")
    table = pd.concat([top_10, bottom_10], ignore_index=True)

    st.dataframe(
        table[
            [
                "rank_group",
                "Category",
                "Sub-Category",
                "total_sales",
                "total_profit",
                "margin_pct",
                "transaction_lines",
            ]
        ].style.format(
            {
                "total_sales": "${:,.0f}",
                "total_profit": "${:,.0f}",
                "margin_pct": "{:.1f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

st.divider()
st.header("What-If Scenario Model")
st.caption(
    "What would happen to profit if we capped discount rates? "
    "The model assumes the same quantity sells at the lower discount (optimistic upper bound). "
    "Actual results depend on customer price sensitivity."
)

# Compute scenarios live from filtered data
filtered["implied_base_sales"] = filtered["Sales"] / (1 - filtered["Discount"])
filtered["cost"] = filtered["Sales"] - filtered["Profit"]

scenarios = [
    ("A - Cap at 30%", 0.30),
    ("B - Cap at 20%", 0.20),
    ("C - Zero discount", 0.00),
]
scenario_rows = []
baseline_profit = filtered["Profit"].sum()
baseline_sales = filtered["Sales"].sum()

for name, cap in scenarios:
    cap_mask = filtered["Discount"] > cap
    n_affected = cap_mask.sum()

    new_sales = filtered["Sales"].copy()
    new_profit = filtered["Profit"].copy()

    new_sales.loc[cap_mask] = (
        filtered.loc[cap_mask, "implied_base_sales"] * (1 - cap)
    )
    new_profit.loc[cap_mask] = new_sales.loc[cap_mask] - filtered.loc[cap_mask, "cost"]

    delta_profit = new_profit.sum() - baseline_profit
    new_margin = new_profit.sum() / new_sales.sum() * 100

    scenario_rows.append({
        "Scenario": name,
        "Total Sales": new_sales.sum(),
        "Total Profit": new_profit.sum(),
        "Margin %": new_margin,
        "Profit Change": delta_profit,
        "Rows Affected": n_affected,
    })

scenario_df = pd.DataFrame(scenario_rows)
baseline_row = pd.DataFrame([{
    "Scenario": "Baseline (current)",
    "Total Sales": baseline_sales,
    "Total Profit": baseline_profit,
    "Margin %": baseline_profit / baseline_sales * 100 if baseline_sales else 0,
    "Profit Change": 0,
    "Rows Affected": 0,
}])
scenario_df = pd.concat([baseline_row, scenario_df], ignore_index=True)

st.dataframe(
    scenario_df.style.format({
        "Total Sales": "${:,.0f}",
        "Total Profit": "${:,.0f}",
        "Margin %": "{:.1f}%",
        "Profit Change": "${:+,.0f}",
        "Rows Affected": "{:,}",
    }),
    use_container_width=True,
    hide_index=True,
)

fig = px.bar(
    scenario_df[scenario_df["Scenario"] != "Baseline (current)"],
    x="Scenario",
    y="Profit Change",
    color="Scenario",
    text_auto="$.0f",
    labels={"Profit Change": "Additional Profit vs Baseline", "Scenario": ""},
)
fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=20, b=10), height=400)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "**Assumptions & limitations:** The model infers cost as Sales minus Profit and assumes "
    "the same quantity is sold at the capped discount. It does not account for customers who "
    "may not purchase at a lower discount rate. For Scenario C (zero discount), all discounted "
    "transactions are recalculated at 0% discount. Results are upper-bound estimates."
)
