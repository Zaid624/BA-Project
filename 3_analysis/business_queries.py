"""Business analysis queries for the Superstore sales and discount project.

The script connects to the PostgreSQL source table, exports each stakeholder
question result to `3_analysis/outputs/`, and writes a de-duplicated analytical
snapshot for dashboarding and tests.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Callable

import psycopg2
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "3_analysis" / "outputs"
SOURCE_TABLE = 'public."Superstore Data"'
CLEANED_SOURCE = f"""
(
    SELECT DISTINCT
        "Ship Mode",
        "Segment",
        "Country",
        "City",
        "State",
        "Postal Code",
        "Region",
        "Category",
        "Sub-Category",
        "Sales",
        "Quantity",
        "Discount",
        "Profit"
    FROM {SOURCE_TABLE}
) AS clean_data
"""


def connect():
    """Open a PostgreSQL connection using the project `.env` file."""
    load_dotenv(PROJECT_ROOT / ".env")
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is missing. Add it to the project .env file.")
    return psycopg2.connect(database_url)


def export_query(cursor, filename: str, sql: str) -> list[tuple]:
    """Run a SQL query and export the result set as a CSV file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cursor.execute(sql)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    output_path = OUTPUT_DIR / filename
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"Exported {filename}: {len(rows)} rows")
    return rows


def export_cleaned_snapshot(cursor) -> None:
    """Business question: what clean transaction-level dataset should downstream users consume?"""
    sql = f"""
    SELECT DISTINCT
        "Ship Mode",
        "Segment",
        "Country",
        "City",
        "State",
        "Postal Code",
        "Region",
        "Category",
        "Sub-Category",
        "Sales",
        "Quantity",
        "Discount",
        "Profit"
    FROM {CLEANED_SOURCE}
    ORDER BY
        "Region", "State", "City", "Category", "Sub-Category",
        "Sales", "Quantity", "Discount", "Profit"
    """
    export_query(cursor, "superstore_cleaned.csv", sql)


def query_top_profitable_subcategories(cursor) -> list[tuple]:
    """Business question: which sub-categories generate the highest total profit?"""
    sql = f"""
    SELECT
        "Sub-Category" AS sub_category,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct
    FROM {CLEANED_SOURCE}
    GROUP BY "Sub-Category"
    ORDER BY total_profit DESC
    LIMIT 10
    """
    return export_query(cursor, "01_top_profitable_subcategories.csv", sql)


def query_bottom_loss_subcategories(cursor) -> list[tuple]:
    """Business question: which sub-categories lose money or produce the weakest profit?"""
    sql = f"""
    SELECT
        "Sub-Category" AS sub_category,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct
    FROM {CLEANED_SOURCE}
    GROUP BY "Sub-Category"
    ORDER BY total_profit ASC
    LIMIT 10
    """
    return export_query(cursor, "02_bottom_loss_subcategories.csv", sql)


def query_sales_profit_by_region(cursor) -> list[tuple]:
    """Business question: which regions generate the most sales and profit?"""
    sql = f"""
    SELECT
        "Region" AS region,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct,
        ROUND(AVG("Discount")::numeric, 3) AS avg_discount,
        COUNT(*) AS transaction_lines
    FROM {CLEANED_SOURCE}
    GROUP BY "Region"
    ORDER BY total_sales DESC
    """
    return export_query(cursor, "03_sales_profit_by_region.csv", sql)


def query_sales_profit_by_category(cursor) -> list[tuple]:
    """Business question: which product categories contribute the most sales, profit, and margin?"""
    sql = f"""
    SELECT
        "Category" AS category,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct,
        COUNT(*) AS transaction_lines
    FROM {CLEANED_SOURCE}
    GROUP BY "Category"
    ORDER BY total_sales DESC
    """
    return export_query(cursor, "04_sales_profit_by_category.csv", sql)


def query_performance_by_segment(cursor) -> list[tuple]:
    """Business question: which customer segments generate the most sales and profit?"""
    sql = f"""
    SELECT
        "Segment" AS segment,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct,
        ROUND(AVG("Sales")::numeric, 2) AS avg_transaction_line_value,
        COUNT(*) AS transaction_lines
    FROM {CLEANED_SOURCE}
    GROUP BY "Segment"
    ORDER BY total_sales DESC
    """
    return export_query(cursor, "05_performance_by_segment.csv", sql)


def query_top_profitable_states(cursor) -> list[tuple]:
    """Business question: which states are the strongest profit contributors?"""
    sql = f"""
    SELECT
        "State" AS state,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct,
        COUNT(*) AS transaction_lines
    FROM {CLEANED_SOURCE}
    GROUP BY "State"
    ORDER BY total_profit DESC
    LIMIT 10
    """
    return export_query(cursor, "06_top_profitable_states.csv", sql)


def query_bottom_loss_states(cursor) -> list[tuple]:
    """Business question: which states are reducing profit and need sales-policy review?"""
    sql = f"""
    SELECT
        "State" AS state,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct,
        COUNT(*) AS transaction_lines
    FROM {CLEANED_SOURCE}
    GROUP BY "State"
    ORDER BY total_profit ASC
    LIMIT 10
    """
    return export_query(cursor, "07_bottom_loss_states.csv", sql)


def query_discount_impact(cursor) -> list[tuple]:
    """Business question: at which discount levels does the business become loss-making?"""
    sql = f"""
    SELECT
        CASE
            WHEN "Discount" = 0 THEN '0%'
            WHEN "Discount" <= 0.1 THEN '1-10%'
            WHEN "Discount" <= 0.2 THEN '11-20%'
            WHEN "Discount" <= 0.3 THEN '21-30%'
            WHEN "Discount" <= 0.4 THEN '31-40%'
            WHEN "Discount" <= 0.5 THEN '41-50%'
            WHEN "Discount" <= 0.6 THEN '51-60%'
            ELSE '60%+'
        END AS discount_band,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct,
        COUNT(*) AS transaction_lines,
        MIN("Discount") AS min_discount,
        MAX("Discount") AS max_discount
    FROM {CLEANED_SOURCE}
    -- The CASE statement standardizes individual discount rates into commercial policy bands.
    GROUP BY discount_band
    ORDER BY MIN("Discount")
    """
    return export_query(cursor, "08_discount_impact.csv", sql)


def query_highest_sales_lines(cursor) -> list[tuple]:
    """Business question: are the highest-revenue transaction lines also profitable?"""
    sql = f"""
    SELECT
        "Category" AS category,
        "Sub-Category" AS sub_category,
        ROUND("Sales"::numeric, 2) AS sales,
        "Quantity" AS quantity,
        "Discount" AS discount,
        ROUND("Profit"::numeric, 2) AS profit,
        ROUND(("Profit" / NULLIF("Sales", 0) * 100)::numeric, 2) AS margin_pct,
        "Region" AS region,
        "State" AS state,
        "City" AS city
    FROM {CLEANED_SOURCE}
    ORDER BY "Sales" DESC
    LIMIT 10
    """
    return export_query(cursor, "09_highest_sales_transaction_lines.csv", sql)


def query_shipping_mode_by_category(cursor) -> list[tuple]:
    """Business question: which shipping modes are most frequently used by category?"""
    sql = f"""
    SELECT
        "Category" AS category,
        "Ship Mode" AS ship_mode,
        COUNT(*) AS transaction_lines,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit
    FROM {CLEANED_SOURCE}
    GROUP BY "Category", "Ship Mode"
    ORDER BY "Category", transaction_lines DESC
    """
    return export_query(cursor, "10_shipping_mode_by_category.csv", sql)


def query_top_cities_by_sales(cursor) -> list[tuple]:
    """Business question: which cities generate the highest sales, and are they profitable?"""
    sql = f"""
    SELECT
        "City" AS city,
        "State" AS state,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct,
        COUNT(*) AS transaction_lines
    FROM {CLEANED_SOURCE}
    GROUP BY "City", "State"
    ORDER BY total_sales DESC
    LIMIT 10
    """
    return export_query(cursor, "11_top_cities_by_sales.csv", sql)


def query_top_subcategories_by_region(cursor) -> list[tuple]:
    """Business question: which sub-categories drive sales in each region?"""
    sql = f"""
    SELECT
        ranked.region,
        ranked.sub_category,
        ranked.total_sales,
        ranked.total_profit,
        ranked.margin_pct,
        ranked.sales_rank
    FROM (
        SELECT
            "Region" AS region,
            "Sub-Category" AS sub_category,
            ROUND(SUM("Sales")::numeric, 2) AS total_sales,
            ROUND(SUM("Profit")::numeric, 2) AS total_profit,
            ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS margin_pct,
            ROW_NUMBER() OVER (PARTITION BY "Region" ORDER BY SUM("Sales") DESC) AS sales_rank
        FROM {CLEANED_SOURCE}
        GROUP BY "Region", "Sub-Category"
    ) ranked
    -- The window function ranks sub-categories within each region before filtering to the top five.
    WHERE ranked.sales_rank <= 5
    ORDER BY ranked.region, ranked.sales_rank
    """
    return export_query(cursor, "12_top_subcategories_by_region.csv", sql)


def query_quantity_by_subcategory(cursor) -> list[tuple]:
    """Business question: which sub-categories are bought in the highest quantity?"""
    sql = f"""
    SELECT
        "Category" AS category,
        "Sub-Category" AS sub_category,
        SUM("Quantity") AS units_sold,
        COUNT(*) AS transaction_lines,
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit
    FROM {CLEANED_SOURCE}
    GROUP BY "Category", "Sub-Category"
    ORDER BY units_sold DESC
    LIMIT 10
    """
    return export_query(cursor, "13_quantity_by_subcategory.csv", sql)


def query_avg_value_by_region_segment(cursor) -> list[tuple]:
    """Business question: how does average transaction value differ by region and segment?"""
    sql = f"""
    SELECT
        "Region" AS region,
        "Segment" AS segment,
        ROUND(AVG("Sales")::numeric, 2) AS avg_transaction_line_value,
        ROUND(AVG("Profit")::numeric, 2) AS avg_profit_per_line,
        COUNT(*) AS transaction_lines
    FROM {CLEANED_SOURCE}
    GROUP BY "Region", "Segment"
    ORDER BY "Region", avg_transaction_line_value DESC
    """
    return export_query(cursor, "14_avg_value_by_region_segment.csv", sql)


def query_overall_business_kpis(cursor) -> list[tuple]:
    """Business question: what is the overall commercial baseline for sales, profit, and margin?"""
    sql = f"""
    SELECT
        ROUND(SUM("Sales")::numeric, 2) AS total_sales,
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        ROUND((SUM("Profit") / NULLIF(SUM("Sales"), 0) * 100)::numeric, 2) AS overall_margin_pct,
        ROUND(AVG("Discount")::numeric, 4) AS avg_discount,
        SUM("Quantity") AS total_units_sold,
        COUNT(*) AS transaction_lines,
        ROUND((SUM("Sales") / COUNT(*))::numeric, 2) AS avg_transaction_line_value
    FROM {CLEANED_SOURCE}
    """
    return export_query(cursor, "15_overall_business_kpis.csv", sql)


def main() -> None:
    queries: list[Callable] = [
        export_cleaned_snapshot,
        query_top_profitable_subcategories,
        query_bottom_loss_subcategories,
        query_sales_profit_by_region,
        query_sales_profit_by_category,
        query_performance_by_segment,
        query_top_profitable_states,
        query_bottom_loss_states,
        query_discount_impact,
        query_highest_sales_lines,
        query_shipping_mode_by_category,
        query_top_cities_by_sales,
        query_top_subcategories_by_region,
        query_quantity_by_subcategory,
        query_avg_value_by_region_segment,
        query_overall_business_kpis,
    ]

    with connect() as connection:
        with connection.cursor() as cursor:
            for query in queries:
                query(cursor)

    print("All business query exports completed.")


if __name__ == "__main__":
    main()
