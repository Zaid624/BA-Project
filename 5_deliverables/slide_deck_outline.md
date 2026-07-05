# Slide Deck Outline

## 1. Title

Sales Discount Strategy Analysis  
How discounting, region, and product mix affect profitability in a retail sales dataset

## 2. Business Problem

Chart: KPI cards for total sales, total profit, margin %, and transaction lines.  
Takeaway: The business generated $2,296,195.59 in sales and $286,241.42 in profit, but margin performance varies strongly by discount level, region, and category.

## 3. Approach and Data

Chart: Simple data flow from PostgreSQL source table to cleaned CSV outputs, Streamlit dashboard, and Power BI-ready exports.  
Takeaway: The analysis uses 9,977 distinct transaction lines after removing 17 exact duplicate records from the 9,994-row source table.

## 4. Finding: Discount Threshold

Chart: Profit and margin by discount band.  
Takeaway: Discounts above 20% are collectively loss-making; the 60%+ discount band lost $70,608.16 at a -122.63% margin.

## 5. Finding: Category & Product Margin Gaps

Chart: Profit by category (bar) + bottom sub-categories and states.  
Takeaway: Technology (17.40% margin) outperforms Furniture (2.49%) by a wide margin. Tables alone lost $17,725 and Texas lost $25,751.

## 6. Finding: What-If Scenario Impact

Chart: Bar chart comparing additional profit per scenario (cap at 30%, cap at 20%, zero discount).  
Takeaway: Capping discounts at 20% could increase profit by $219,140 (+77%) and lift margin from 12.47% to 20.09%.

## 7. Forecast (Methodology Demo)

Chart: 12-month sales forecast with historical vs projected line.  
Takeaway: The forecast pipeline demonstrates time-series methodology using synthetic dates (MAPE: 7.8%). The model captures realistic Q4 seasonality. Forecasts are not actionable until real dates are available.

## 8. Recommendations and Next Steps

Chart: Action priority matrix by impact and feasibility.  
Takeaway: Tighten approval for discounts above 20%, launch a Furniture margin review, run the what-if scenario model for different discount caps, and request date, customer, campaign, and cost data for deeper analysis.
