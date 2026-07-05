# Privacy-by-Design Notes (DSGVO / GDPR)

**Context:** The analysis in this project used a public sample dataset (Superstore) with no personally identifiable information. This document outlines how the same analysis would be handled if it involved real customer data, applying privacy-by-design principles from the outset.

---

## Data Minimization

Only fields required for the stated business purpose were included in the analytical snapshot (region, category, sales, profit, discount, quantity, shipping mode, segment). If the source contained customer names, email addresses, or account numbers, those fields would be excluded from the analysis dataset at extraction time — not after the fact.

## Purpose Limitation

The data was used exclusively for margin and discount-policy analysis as commissioned by the Head of Sales. No customer profiling, retention scoring, or ad-targeting analysis was performed or would be performed on this dataset without a separate documented purpose and renewed consent check.

## Pseudonymization

In a live-data scenario, direct identifiers (customer name, email, account ID) would be replaced with a pseudonymous key before the analytical snapshot is created. The mapping table would be stored separately with restricted access and a defined deletion date. The analysis itself would operate only on the pseudonymized dataset.

## Retention

The analytical snapshot would be retained only for the duration of the project plus a documented review period (e.g., 12 months after the final report). After that, the pseudonymized dataset would be deleted or aggregated to a level where individual transactions can no longer be reconstructed. The original source data would remain in the operational system under its own retention policy.

## Access Control

Role-based access:
- **Analyst** (me): can read pseudonymized snapshot, cannot re-identify individuals
- **Sales leadership**: can read aggregated dashboards and reports only
- **Data steward**: holds the pseudonymization mapping, manages retention

No raw customer-identifiable data is accessible in the analysis environment.

## DSGVO Compliance Note

If this project were conducted with data of EU data subjects, the following additional measures would apply:

- **Art. 5** (principles): documented purpose limitation and data minimization as described above
- **Art. 25** (data protection by design): pseudonymization built into the extraction pipeline, not bolted on after the fact
- **Art. 32** (security): encrypted storage for the snapshot, role-based access, audit logging of all queries that return >100 rows
- **Art. 33** (breach notification): incident response process documented in the project handover
- **Data Processing Agreement (DPA)**: in place with any third-party tools used (database hosting, BI platforms)

Re-identification of pseudonymized records would require explicit documented approval and would be logged.

---

*This document is a signal of methodology awareness, not a legal opinion. For production deployment, consult the organisation's Data Protection Officer.*
