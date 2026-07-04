# Power BI Dashboard Build Guide

This folder contains clean, pre-aggregated CSV exports for building a Power BI version of the dashboard:

- `by_region.csv`
- `by_category.csv`
- `by_discount_band.csv`
- `by_ship_mode_segment.csv`

The requested monthly export cannot be created from the inspected source data because there is no `Order Date`, `Ship Date`, month, year, or equivalent date column. If a date field is added later, create a `by_month.csv` export grouped by calendar month and use the time-series steps below.

## 1. Load the Data

1. Open Power BI Desktop.
2. Select **Get data > Text/CSV**.
3. Import the four CSV files from `4_dashboard/powerbi_export/`.
4. Set numeric columns such as `total_sales`, `total_profit`, `margin_pct`, `avg_discount`, and `transaction_lines` to decimal number or whole number as appropriate.
5. Do not create relationships between these aggregate tables unless you later add a shared dimension model. For this portfolio dashboard, each visual can use its corresponding aggregate table.

## 2. Core DAX Measures

Create these measures in a dedicated measures table or in the main aggregate table you use for KPI cards:

```DAX
Total Sales = SUM(by_region[total_sales])

Total Profit = SUM(by_region[total_profit])

Margin % = DIVIDE([Total Profit], [Total Sales])

Transaction Lines = SUM(by_region[transaction_lines])

Average Discount = AVERAGE(by_region[avg_discount])
```

Format `Total Sales` and `Total Profit` as currency, `Margin %` and `Average Discount` as percentages, and `Transaction Lines` as a whole number.

## 3. Dashboard Layout

1. Add four KPI cards across the top:
   - Total Sales
   - Total Profit
   - Margin %
   - Transaction Lines
2. Add slicers for `region` and `category` where relevant.
3. Add a clustered bar chart using `by_category.csv`:
   - Axis: `category`
   - Values: `total_profit`
   - Tooltip: `total_sales`, `margin_pct`, `transaction_lines`
4. Add a bar chart using `by_region.csv`:
   - Axis: `region`
   - Values: `total_sales` and `total_profit`
   - Tooltip: `margin_pct`, `avg_discount`
5. Add a column or line chart using `by_discount_band.csv`:
   - Axis: `discount_band`
   - Values: `total_profit`
   - Tooltip: `total_sales`, `margin_pct`, `transaction_lines`
6. Add a matrix using `by_ship_mode_segment.csv`:
   - Rows: `ship_mode`
   - Columns: `segment`
   - Values: `total_sales`, `total_profit`, `transaction_lines`

## 4. Time-Series Extension if Date Data Becomes Available

If a future source extract includes `Order Date`, add a `by_month.csv` table with `month`, `total_sales`, `total_profit`, and `margin_pct`. Then create a line chart:

- X-axis: `month`
- Y-axis: `total_sales`
- Tooltip: `total_profit`, `margin_pct`

Recommended DAX measure:

```DAX
Monthly Sales = SUM(by_month[total_sales])
```

This step is deliberately not included in the current build because using a fake or row-order-based month would make the analysis misleading.
