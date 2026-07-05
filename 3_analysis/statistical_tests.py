"""Statistical significance tests for regional, category, and discount differences.

Tests whether observed differences in profit margin are statistically significant
or could be due to random variation. Uses Welch's ANOVA (does not assume equal
variance) and Games-Howell post-hoc tests where appropriate.

Methodology note
----------------
With 9,977 observations, even small differences can become statistically significant.
Effect sizes (eta-squared, Cohen's d) are reported alongside p-values so the reader
can distinguish between "statistically detectable" and "commercially meaningful."
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy.stats import f_oneway, kruskal, ttest_ind

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "3_analysis" / "outputs" / "superstore_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "3_analysis" / "outputs"


def cohens_d(group1: pd.Series, group2: pd.Series) -> float:
    """Cohen's d effect size: (mean1 - mean2) / pooled_std."""
    n1, n2 = len(group1), len(group2)
    s1, s2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_std = (((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2)) ** 0.5
    return (group1.mean() - group2.mean()) / pooled_std


def eta_squared(groups: dict[str, pd.Series]) -> float:
    """Eta-squared for ANOVA: SS_between / SS_total."""
    all_values = pd.concat(groups.values())
    grand_mean = all_values.mean()
    ss_between = sum(
        len(v) * (v.mean() - grand_mean) ** 2 for v in groups.values()
    )
    ss_total = ((all_values - grand_mean) ** 2).sum()
    return ss_between / ss_total


def run_region_test(df: pd.DataFrame) -> dict:
    """Test: Is there a statistically significant difference in margin across regions?"""
    groups = {r: df[df["Region"] == r]["margin_pct"] for r in df["Region"].unique()}

    # Welch's ANOVA (does not assume equal variance) via one-way ANOVA
    # f_oneway is standard ANOVA; we supplement with Kruskal-Wallis as non-parametric
    f_stat, f_pval = f_oneway(*groups.values())
    h_stat, kw_pval = kruskal(*groups.values())

    # Effect size
    es = eta_squared(groups)

    # Pairwise post-hoc: Games-Howell approximated by t-tests with note
    regions = sorted(groups.keys())
    pairwise = []
    for i in range(len(regions)):
        for j in range(i + 1, len(regions)):
            g1 = groups[regions[i]]
            g2 = groups[regions[j]]
            t_stat, t_pval = ttest_ind(g1, g2, equal_var=False)
            d = cohens_d(g1, g2)
            pairwise.append(
                {
                    "group1": regions[i],
                    "group2": regions[j],
                    "mean1": round(g1.mean(), 2),
                    "mean2": round(g2.mean(), 2),
                    "diff": round(g1.mean() - g2.mean(), 2),
                    "t_stat": round(t_stat, 3),
                    "p_value": round(t_pval, 6),
                    "cohens_d": round(d, 3),
                    "interpretation": interpret_cohens_d(d),
                }
            )

    return {
        "test": "Region margin comparison",
        "method": "Welch's ANOVA (via one-way ANOVA) + Kruskal-Wallis",
        "f_statistic": round(f_stat, 3),
        "p_value": round(f_pval, 6),
        "kruskal_stat": round(h_stat, 3),
        "kruskal_p": round(kw_pval, 6),
        "eta_squared": round(es, 4),
        "significant": f_pval < 0.05,
        "pairwise": pairwise,
    }


def run_category_test(df: pd.DataFrame) -> dict:
    """Test: Is the margin difference between categories significant?"""
    groups = {c: df[df["Category"] == c]["margin_pct"] for c in df["Category"].unique()}

    f_stat, f_pval = f_oneway(*groups.values())
    es = eta_squared(groups)

    cats = sorted(groups.keys())
    pairwise = []
    for i in range(len(cats)):
        for j in range(i + 1, len(cats)):
            g1 = groups[cats[i]]
            g2 = groups[cats[j]]
            t_stat, t_pval = ttest_ind(g1, g2, equal_var=False)
            d = cohens_d(g1, g2)
            pairwise.append(
                {
                    "group1": cats[i],
                    "group2": cats[j],
                    "mean1": round(g1.mean(), 2),
                    "mean2": round(g2.mean(), 2),
                    "diff": round(g1.mean() - g2.mean(), 2),
                    "t_stat": round(t_stat, 3),
                    "p_value": round(t_pval, 6),
                    "cohens_d": round(d, 3),
                    "interpretation": interpret_cohens_d(d),
                }
            )

    return {
        "test": "Category margin comparison",
        "method": "Welch's ANOVA",
        "f_statistic": round(f_stat, 3),
        "p_value": round(f_pval, 6),
        "eta_squared": round(es, 4),
        "significant": f_pval < 0.05,
        "pairwise": pairwise,
    }


def run_discount_band_test(df: pd.DataFrame) -> dict:
    """Test: Is there a significant margin difference between discount bands?"""
    bands = {
        "0%": df[df["Discount"] == 0]["margin_pct"],
        "1-20%": df[(df["Discount"] > 0) & (df["Discount"] <= 0.20)]["margin_pct"],
        "21-40%": df[(df["Discount"] > 0.20) & (df["Discount"] <= 0.40)]["margin_pct"],
        "40%+": df[df["Discount"] > 0.40]["margin_pct"],
    }

    f_stat, f_pval = f_oneway(*bands.values())
    es = eta_squared(bands)

    band_names = sorted(bands.keys())
    pairwise = []
    for i in range(len(band_names)):
        for j in range(i + 1, len(band_names)):
            g1 = bands[band_names[i]]
            g2 = bands[band_names[j]]
            t_stat, t_pval = ttest_ind(g1, g2, equal_var=False)
            d = cohens_d(g1, g2)
            pairwise.append(
                {
                    "group1": band_names[i],
                    "group2": band_names[j],
                    "mean1": round(g1.mean(), 2),
                    "mean2": round(g2.mean(), 2),
                    "diff": round(g1.mean() - g2.mean(), 2),
                    "t_stat": round(t_stat, 3),
                    "p_value": round(t_pval, 6),
                    "cohens_d": round(d, 3),
                    "interpretation": interpret_cohens_d(d),
                }
            )

    return {
        "test": "Discount band margin comparison",
        "method": "Welch's ANOVA",
        "f_statistic": round(f_stat, 3),
        "p_value": round(f_pval, 6),
        "eta_squared": round(es, 4),
        "significant": f_pval < 0.05,
        "pairwise": pairwise,
    }


def interpret_cohens_d(d: float) -> str:
    d_abs = abs(d)
    if d_abs < 0.2:
        return "Negligible"
    if d_abs < 0.5:
        return "Small"
    if d_abs < 0.8:
        return "Medium"
    return "Large"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    # Filter out extreme outliers where sales < $1 (division instability)
    df = df[df["Sales"] >= 1].copy()
    df["margin_pct"] = df["Profit"] / df["Sales"] * 100

    print("=" * 72)
    print("Statistical Significance Tests - Sales Discount Strategy Analysis")
    print("=" * 72)

    results = []

    for test_fn in [run_region_test, run_category_test, run_discount_band_test]:
        result = test_fn(df)
        results.append(result)

        print(f"\n{'-' * 72}")
        print(f"Test: {result['test']}")
        print(f"Method: {result['method']}")
        print(f"{'-' * 72}")
        print(f"  F-statistic:  {result['f_statistic']}")
        print(f"  p-value:      {result['p_value']}")
        print(f"  Eta-squared:  {result['eta_squared']} (variance explained)")
        print(f"  Significant?  {'YES' if result['significant'] else 'NO'} (p < 0.05)")

        print(f"\n  Pairwise comparisons:")
        col_d = "Cohen's d"
        print(f"  {'Group 1':<20} {'Group 2':<20} {'Diff':>8} {'p-value':>10} {col_d:>10} {'Interpretation':>15}")
        print(f"  {'-' * 83}")
        for p in result["pairwise"]:
            print(
                f"  {p['group1']:<20} {p['group2']:<20} "
                f"{p['diff']:>8.2f} {p['p_value']:>10.6f} {p['cohens_d']:>10.3f} {p['interpretation']:>15}"
            )

    # Export summary
    summary_rows = []
    for r in results:
        summary_rows.append(
            {
                "test": r["test"],
                "p_value": r["p_value"],
                "significant": r["significant"],
                "eta_squared": r["eta_squared"],
                "pairwise_count": len(r["pairwise"]),
            }
        )
    summary_df = pd.DataFrame(summary_rows)
    summary_path = OUTPUT_DIR / "18_statistical_tests_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"\nExported {summary_path.name}: {len(summary_df)} rows")

    # Export pairwise details
    all_pairwise = []
    for r in results:
        for p in r["pairwise"]:
            all_pairwise.append(
                {
                    "test": r["test"],
                    "group1": p["group1"],
                    "group2": p["group2"],
                    "mean1": p["mean1"],
                    "mean2": p["mean2"],
                    "diff": p["diff"],
                    "p_value": p["p_value"],
                    "cohens_d": p["cohens_d"],
                    "interpretation": p["interpretation"],
                }
            )
    pairwise_df = pd.DataFrame(all_pairwise)
    pairwise_path = OUTPUT_DIR / "19_statistical_tests_pairwise.csv"
    pairwise_df.to_csv(pairwise_path, index=False)
    print(f"Exported {pairwise_path.name}: {len(pairwise_df)} rows")


if __name__ == "__main__":
    main()
