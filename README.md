# Sales Discount Strategy Analysis

**One-line pitch:** A Business Analyst portfolio project tracing where $2.30M in retail sales translates into profit — and where discounting erodes it — using SQL, Python, Streamlit, and Power BI-ready exports.

---

## The Business Problem

The Head of Sales needed to know: *Is our discounting strategy working?* Sales volume alone doesn't explain performance. This project analyzes 9,977 transaction lines across 4 regions, 3 categories, and 17 sub-categories to identify where discounts, product mix, and geography drive or destroy margin.

## What I Did

| Layer | Deliverable |
|---|---|
| **Business case** | Problem statement framed for a Head of Sales (`1_business_case/`) |
| **Requirements** | Stakeholder questions + data dictionary with GDPR awareness (`2_requirements/`) |
| **Analysis** | 15 SQL/Python queries + what-if scenario model (discount cap simulation), all exporting real results (`3_analysis/`) |
| **Dashboard** | Interactive Streamlit app with KPI cards, scatter plots, and filters (`4_dashboard/`) |
| **Power BI track** | Pre-aggregated CSVs + build guide for Power BI Desktop (`4_dashboard/powerbi_export/`) |
| **Deliverables** | Executive summaries in English + German, slide deck outline, resume bullets, LinkedIn post (`5_deliverables/`) |
| **Testing** | Data-quality tests (pytest) codifying cleaning checks (`tests/`) |

## Headline Finding

**Discounts above 20% are collectively loss-making.** The 60%+ band generated $57,580 in sales but lost $70,608 at a -122.63% margin. By contrast, no-discount lines produced $1,087,278 in sales at 29.51% margin.

## What-If Scenario: Cap Discounts at 20%

The what-if scenario model estimates that capping all discounts at 20% could increase total profit by **$219,140 (+77%)** — from $286,241 to $505,382 — and improve overall margin from 12.47% to 20.09%. Even a moderate 30% cap would add $146,437 in profit. Try it live in the dashboard.

## Dataset Limitations

The source has no order dates, customer IDs, product names, campaign history, or cost-of-goods data. The analysis identifies commercial patterns, not causal proof.

## Tech Stack

Python · PostgreSQL · SQL · Streamlit · Plotly · pandas · pytest · Power BI–ready CSVs

## How to Run

```powershell
# 1. Install dependencies
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2. Regenerate analysis (requires .env with DATABASE_URL)
.venv\Scripts\python.exe 3_analysis\business_queries.py

# 3. Run data-quality tests
.venv\Scripts\python.exe -m pytest

# 4. Launch dashboard
.venv\Scripts\streamlit.exe run 4_dashboard\app.py
```

## Dashboard

The Streamlit app (`4_dashboard/app.py`) provides interactive filtering by region and category with KPI cards, profit-by-category bars, a discount-vs-profit scatter plot, and a top/bottom sub-category table. Deployable on Streamlit Community Cloud.

Live Demo: https://salesstratergy.streamlit.app/

<img width="1728" height="1060" alt="file-69a65db11a3d4d778683a493b83a7ef6" src="https://github.com/user-attachments/assets/f8b60cff-6673-4cb3-b2dd-e1f8cd0f74cb" />
<img width="1727" height="1057" alt="file-ba08b4cd1a93f514c99e69406a1e1af7" src="https://github.com/user-attachments/assets/ccd8b52d-599a-4842-b7d3-8ac11eec02c6" />




## Structure

```
sales-discount-strategy-analysis/
├── 1_business_case/          # Problem statement
├── 2_requirements/           # Stakeholder questions, data dictionary
├── 3_analysis/               # SQL queries, outputs/, data-quality notes
├── 4_dashboard/              # Streamlit app, powerbi_export/
├── 5_deliverables/           # Executive summaries (EN/DE), slide deck, resume, LinkedIn
├── tests/                    # pytest data-quality tests
├── .gitignore
├── requirements.txt
└── README.md
```
