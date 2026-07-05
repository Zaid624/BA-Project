# Sales Forecast — Plain Language Summary

## What we did

The original dataset has no dates — so we couldn't do time-series analysis. To show the methodology, we assigned **synthetic (made-up) dates** to each transaction (Jan 2022 – Dec 2023) and built a forecast model for the next 12 months.

## How it works

We grouped sales by month (24 months of history) and used **linear regression** to find two patterns:
1. **Trend**: are sales going up or down over time?
2. **Seasonality**: are some months consistently higher or lower? (e.g., Q4 holiday spike)

The model then projects these patterns 12 months forward.

## Results (with synthetic dates)

| Metric | Value |
|---|---|
| **Model accuracy** | Average error: $7,060/month (7.8% of actual) |
| **Forecast next 12 months** | $1,155,761 total |
| **vs last 12 months** | +0.4% (essentially flat) |
| **Peak month** | Dec 2024: $149,146 |
| **Low month** | Aug 2024: $71,247 |

The forecast captures a realistic Q4 holiday spike (Oct-Dec is consistently the highest period).

## The honest caveat (important)

> These are synthetic dates. The model shows the **methodology works** — the code, the features, the accuracy metrics are real — but the forecast numbers themselves are not actionable because the dates don't reflect actual order timing.

In a real project with real dates, this exact pipeline would produce a decision-ready forecast.

## What it proves for a BA portfolio

- You can build a time-series model from raw transaction data
- You understand trend vs seasonality decomposition
- You report accuracy metrics honestly
- You clearly state limitations instead of pretending the data is better than it is
