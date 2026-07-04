# Data Dictionary

Source table inspected: `public."Superstore Data"`  
Source row count: 9,994 rows  
Analytical snapshot: 9,977 distinct rows after removing exact duplicate records

| Column | Data type | Example value | Business meaning | Assumption |
|---|---:|---|---|---|
| Ship Mode | text | Second Class | Shipping service selected for the transaction line. | Treated as the fulfillment method for the order line, not as a delivery performance measure. |
| Segment | text | Consumer | Customer segment assigned to the transaction. | Segment labels are assumed to be mutually exclusive commercial customer groups. |
| Country | text | United States | Country where the sale was recorded. | Dataset is U.S.-only in the inspected sample, so country is not used as a comparison dimension. |
| City | text | Henderson | City where the sale was recorded. | Used as a geographic sales dimension; no address-level precision is available. |
| State | text | Kentucky | U.S. state where the sale was recorded. | Used as the main sub-regional profitability dimension. |
| Postal Code | bigint | 42420 | Postal code associated with the transaction location. | Treated as a geographic attribute, not as personally identifiable customer information in this public-style sample. |
| Region | text | South | Sales region assigned to the transaction. | Used for management-level regional comparison. |
| Category | text | Furniture | High-level product category. | Used for portfolio-level sales and margin analysis. |
| Sub-Category | text | Bookcases | More detailed product grouping under category. | Used as the most granular product view because product names are not available. |
| Sales | double precision | 261.96 | Revenue recorded for the transaction line before or after discount as provided by the source data. | Treated as net sales value available for margin calculation. |
| Quantity | bigint | 2 | Number of units sold on the transaction line. | Assumed to represent sold units, not shipped units or returned units. |
| Discount | double precision | 0.0 | Discount rate applied to the transaction line. | Interpreted as a decimal rate, e.g. `0.2` means 20%. |
| Profit | double precision | 41.9136 | Profit recorded for the transaction line. | Treated as contribution profit from the source system; cost breakdown is not available. |

## DSGVO/GDPR Handling Note

The inspected dataset does not include names, email addresses, customer IDs, or street addresses. If the same analysis were run on live customer data, the minimum appropriate handling would include using only fields required for the analysis, replacing direct customer identifiers with anonymized or pseudonymized keys, restricting access to raw data, documenting retention periods, and deleting or aggregating transaction-level data once it is no longer needed for the stated business purpose.
