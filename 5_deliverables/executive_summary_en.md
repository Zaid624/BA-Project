# Executive Summary

## Context

The Head of Sales asked for a fact-based view of where sales growth is translating into profit and where discounting or product mix is eroding margin. The analysis uses a cleaned Superstore transaction snapshot of 9,977 distinct rows covering region, state, city, segment, category, sub-category, sales, quantity, discount, and profit. The dataset does not include order dates, customer IDs, product names, campaign history, or cost-of-goods detail, so the findings should be read as commercial pattern analysis rather than causal proof.

## Key Findings

The strongest finding is that discounts above 20% are collectively loss-making. No-discount transaction lines generated $1,087,277.56 in sales, $320,844.41 in profit, and a 29.51% margin, while the 60%+ discount band generated $57,580.47 in sales but lost $70,608.16, equal to a -122.63% margin.

Regional performance is uneven. The West is the strongest region with $725,255.64 in sales, $108,329.81 in profit, and a 14.94% margin, while Central generated $500,782.85 in sales but only $39,655.88 in profit at a 7.92% margin.

Category mix is a major margin issue. Technology generated $836,154.03 in sales and $145,454.95 in profit at a 17.40% margin, while Furniture generated $741,306.31 in sales but only $18,421.81 in profit at a 2.49% margin.

Losses are concentrated in specific states and sub-categories. Texas lost $25,750.98 on $170,124.54 in sales, and Tables lost $17,725.48 on $206,965.53 in sales.

A what-if scenario model shows that capping discounts at 20% could increase total profit by $219,140 (from $286,241 to $505,382) and improve overall margin from 12.47% to 20.09%. Even a moderate cap at 30% would add $146,437 in profit.

## Recommendations

Introduce stricter approval rules for discounts above 20%, with particular scrutiny for discounts of 60% or more because this band is deeply loss-making in the current data.

Treat Furniture as a margin-recovery priority, especially Tables and Bookcases, by reviewing discount rules, sales incentives, and whether low-margin products should be bundled with more profitable categories.

Use the West, New York, California, Washington, and high-margin sub-categories such as Copiers, Paper, and Accessories as benchmarks for profitable growth playbooks.

Use the what-if scenario model in the dashboard to test different discount caps interactively by region and category. The model estimates that even a moderate 30% cap could add $146,437 to annual profit.

## Open Questions

The dataset does not show whether discounts caused the observed losses or were used to clear difficult products, because there is no campaign, inventory, or cost context.

The dataset has no dates, so the analysis cannot identify seasonality, monthly trend changes, or whether discount behavior improved or worsened over time.
