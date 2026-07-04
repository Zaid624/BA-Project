from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "3_analysis" / "outputs" / "superstore_cleaned.csv"
NOTES_PATH = PROJECT_ROOT / "3_analysis" / "data_quality_notes.md"

KEY_COLUMNS = [
    "Ship Mode",
    "Segment",
    "Country",
    "City",
    "State",
    "Postal Code",
    "Region",
    "Category",
    "Sub-Category",
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
]


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def test_cleaned_snapshot_has_expected_row_count() -> None:
    rows = load_rows()
    assert len(rows) == 9977


def test_key_columns_have_no_null_or_blank_values() -> None:
    rows = load_rows()
    for row in rows:
        for column in KEY_COLUMNS:
            assert row[column] not in ("", None)


def test_cleaned_snapshot_has_no_exact_duplicate_rows() -> None:
    rows = load_rows()
    row_signatures = [tuple(row[column] for column in KEY_COLUMNS) for row in rows]
    assert len(row_signatures) == len(set(row_signatures))


def test_numeric_ranges_match_documented_business_rules() -> None:
    rows = load_rows()
    for row in rows:
        sales = float(row["Sales"])
        quantity = int(row["Quantity"])
        discount = float(row["Discount"])
        assert sales >= 0
        assert quantity > 0
        assert 0 <= discount <= 1


def test_date_gap_is_documented_because_source_has_no_date_column() -> None:
    rows = load_rows()
    assert rows
    assert "Order Date" not in rows[0]
    notes = NOTES_PATH.read_text(encoding="utf-8")
    assert "date-range sanity check cannot be performed" in notes.lower()
