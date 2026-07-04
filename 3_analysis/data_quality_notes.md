# Data Quality Notes

## Source Size

The source table contains 9,994 transaction lines. After removing exact duplicate rows across all available fields, the analytical snapshot contains 9,977 rows. This removes 17 duplicated records while preserving all unique commercial observations.

## Duplicates

The dataset does not contain an `Order ID`, so order-level duplicate testing is not possible. Instead, duplicate handling was performed at full-row level across `Ship Mode`, `Segment`, `Country`, `City`, `State`, `Postal Code`, `Region`, `Category`, `Sub-Category`, `Sales`, `Quantity`, `Discount`, and `Profit`. Exact duplicate rows were removed from the analytical snapshot exported as `3_analysis/outputs/superstore_cleaned.csv`.

## Null Values

No null values were found in the inspected source columns. This means the current analysis does not require imputation, deletion for missing values, or stakeholder assumptions about missing categories, locations, discounts, sales, quantities, or profit values.

## Numeric Range Checks

Sales values range from 0.444 to 22,638.48, profit ranges from -6,599.978 to 8,399.976, discounts range from 0.0 to 0.8, and quantity ranges from 1 to 14 units. No records were found with negative sales, non-positive quantity, or discount values outside the expected 0 to 1 range.

## Date-Range Sanity Check

A date-range sanity check cannot be performed because the actual source table does not include `Order Date`, `Ship Date`, month, year, or any other date field. This is a material dataset limitation: the project cannot support seasonality, monthly performance, delivery-time analysis, or before/after discount policy comparisons without an additional date column.

## Other Cleaning Decisions

The dataset contains 4 regions, 49 states, 531 cities, 3 categories, and 17 sub-categories. `Country` is retained for completeness, but because the inspected data is U.S.-only it is not used as a comparison dimension. Postal code is treated only as a geographic attribute; no customer-level identifier is available.
