# Product Backlog — Sales Discount Strategy

**Epic grouping:** Discount Policy | Category Margin | Data Foundation | Monitoring

---

## Epic 1: Discount Policy Reform

> **Data trigger:** Discounts above 20% are collectively loss-making. The 60%+ band lost $70,608 at -122.63% margin. Capping at 20% could add $219,140 profit (+77%).

---

### US-001 — Auto-approve discounts under 20%

| Field | Value |
|---|---|
| **Story** | As Head of Sales, I want discounts under 20% to be auto-approved in the order system so that reps close low-risk deals without friction. |
| **Priority** | High |
| **Story points** | 5 |
| **Epic** | Discount Policy Reform |

**Acceptance criteria:**
- Orders with discount rate < 20% are approved without manager intervention
- The system logs the discount and order ID for monthly audit
- Approval takes less than 2 seconds end-to-end
- Rep receives a confirmation notification

---

### US-002 — Management approval for 20-40% discounts

| Field | Value |
|---|---|
| **Story** | As Head of Sales, I want discounts between 20% and 40% to require regional sales manager approval so that margin-eroding deals are reviewed before they reach the customer. |
| **Priority** | High |
| **Story points** | 8 |
| **Epic** | Discount Policy Reform |

**Acceptance criteria:**
- Discount between 20% and 40% triggers an approval request to the regional manager
- Manager receives notification within 30 seconds
- Approval or rejection is logged with timestamp and manager ID
- Unapproved orders expire after 4 hours
- Monthly report shows approval rate and average discount applied

---

### US-003 — VP-level sign-off for 40%+ discounts

| Field | Value |
|---|---|
| **Story** | As Head of Sales, I want discounts above 40% to require VP-level approval so that deeply loss-making discounts are only granted with explicit commercial justification. |
| **Priority** | High |
| **Story points** | 8 |
| **Epic** | Discount Policy Reform |

**Acceptance criteria:**
- Discount at or above 40% triggers an approval request to the VP of Sales
- Rep must submit a free-text justification (minimum 50 characters)
- Approved exceptions are reviewed in a quarterly governance meeting
- Dashboard tracks number of 40%+ exceptions per quarter by region and category
- VP receives a weekly summary of all exceptions approved

---

## Epic 2: Category Margin Recovery

> **Data trigger:** Furniture generates $741,306 in sales but only $18,422 profit (2.49% margin). Tables alone lost $17,725. Technology delivers 17.40% margin by comparison.

---

### US-004 — Furniture margin deep-dive

| Field | Value |
|---|---|
| **Story** | As Category Manager for Furniture, I want a root-cause analysis for Tables and Bookcases so that I can identify whether pricing, cost, or discounting drives the negative margin. |
| **Priority** | Medium |
| **Story points** | 13 |
| **Epic** | Category Margin Recovery |

**Acceptance criteria:**
- Analysis report covers Tables ($206,965 sales, -$17,725 profit, -8.56% margin)
- Analysis report covers Bookcases ($114,880 sales, -$3,473 profit, -3.02% margin)
- Report breaks down profit by discount band, region, and quarter (if date data available)
- At least three actionable recommendations delivered
- Review meeting scheduled within 2 weeks of report delivery

---

### US-005 — High-margin bundle pilot

| Field | Value |
|---|---|
| **Story** | As Category Manager, I want to pilot bundled offers pairing Furniture with high-margin Accessories (25.05% margin) so that overall category profit improves without requiring individual price increases. |
| **Priority** | Medium |
| **Story points** | 8 |
| **Epic** | Category Margin Recovery |

**Acceptance criteria:**
- Three bundle combinations defined (e.g., Chair + Accessories, Table + Paper)
- Bundle price set at 5-10% discount vs individual items
- Pilot runs for 8 weeks in top-3 cities by sales volume
- Success metric: bundle margin >= 12% (vs current Furniture margin of 2.49%)
- Control group exists for comparison
- Results documented and presented to Category Director

---

## Epic 3: Data Foundation

> **Data trigger:** The current dataset has no order dates, customer IDs, product names, or cost-of-goods data. This blocks time-series analysis, customer segmentation, and campaign attribution.

---

### US-006 — Add date fields to source data

| Field | Value |
|---|---|
| **Story** | As a Business Analyst, I want order date and ship date included in the data extract so that the team can track seasonality, month-over-month discount trends, and delivery performance. |
| **Priority** | High |
| **Story points** | 5 |
| **Epic** | Data Foundation |

**Acceptance criteria:**
- Source extract includes Order Date and Ship Date with every row
- Dates are in ISO 8601 format (YYYY-MM-DD)
- No null date values in the extract
- Monthly trend dashboard is updated with date-dependent charts
- Historical backfill of 12 months of date data completed

---

### US-007 — Automated data quality pipeline

| Field | Value |
|---|---|
| **Story** | As a Business Analyst, I want the cleaning checks from the analysis project to run automatically on each new data load so that downstream reports always use consistent, validated data. |
| **Priority** | Medium |
| **Story points** | 8 |
| **Epic** | Data Foundation |

**Acceptance criteria:**
- Pipeline runs on every new extract or on a scheduled weekly basis
- Checks: duplicate rows, null values in key columns, numeric range validation, discount range 0-1
- Failed checks trigger an email alert to the analytics team
- A log file records pass/fail status per check with row counts
- Pipeline completes within 10 minutes for up to 50,000 rows

---

## Epic 4: Monitoring & Reporting

---

### US-008 — Monthly margin dashboard

| Field | Value |
|---|---|
| **Story** | As Head of Sales, I want a monthly dashboard showing margin, discount usage, and sales by region and category so that I can monitor policy compliance and identify emerging issues. |
| **Priority** | Medium |
| **Story points** | 13 |
| **Epic** | Monitoring & Reporting |

**Acceptance criteria:**
- Dashboard refreshes monthly within 3 business days of month-end
- Pages: Executive Summary, Regional Deep-Dive, Category Analysis, Discount Compliance
- KPI cards: Total Sales, Total Profit, Margin %, % of orders with discount > 20%
- Filters: Region, Category, Month
- Exports to PDF and Excel
- Dashboard is accessible to Sales Directors and above

---

### US-009 — Real-time discount alert

| Field | Value |
|---|---|
| **Story** | As a Sales Director, I want a real-time alert when any region's average weekly discount exceeds 20% so that I can intervene before margin erosion becomes systemic. |
| **Priority** | Low |
| **Story points** | 13 |
| **Epic** | Monitoring & Reporting |

**Acceptance criteria:**
- Alert triggers when rolling 7-day average discount in any region exceeds 20%
- Alert sent via email and in-app notification to the regional Sales Director
- Alert includes: region name, current average discount, transaction count, comparison to prior week
- Same alert criteria available per category (optional configuration)
- Alert threshold configurable by admin (default: 20%)
