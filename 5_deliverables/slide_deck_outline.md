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

## 5. Finding: Regional Performance

Chart: Sales and profit by region.  
Takeaway: West leads with $725,255.64 in sales and $108,329.81 in profit, while Central has the weakest margin at 7.92%.

## 6. Finding: Category Margin Gap

Chart: Profit by category with margin labels.  
Takeaway: Technology delivers a 17.40% margin, while Furniture produces only 2.49% despite $741,306.31 in sales.

## 7. Finding: Concentrated Loss Areas

Chart: Bottom 10 states or sub-categories by profit.  
Takeaway: Texas lost $25,750.98 and Tables lost $17,725.48, making them priority areas for pricing and discount review.

## 8. Recommendations and Next Steps

Chart: Action priority matrix by impact and feasibility.  
Takeaway: Tighten approval for discounts above 20%, launch a Furniture margin review, and request date, customer, campaign, and cost data for deeper analysis.
