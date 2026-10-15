"""Tests for sales report automation."""
import csv
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from main import read_raw, clean_row, summarise

RAW = Path(__file__).parent / "sample_raw_sales.csv"

def test_read_raw():
    rows = read_raw(RAW)
    assert len(rows) == 19  # actual rows in generated CSV
    assert set(rows[0].keys()) == {"date","product","category","region","quantity","unit_price","sales_rep","notes"}

def test_clean_row_drops_zero_qty():
    raw = dict(date="2024-01-01", product="X", category="Y", region="West",
               quantity="0", unit_price="10", sales_rep="Alice", notes="")
    assert clean_row(raw, 0) is None

def test_clean_row_drops_negative_qty():
    raw = dict(date="2024-01-01", product="X", category="Y", region="West",
               quantity="-1", unit_price="10", sales_rep="Alice", notes="")
    assert clean_row(raw, 0) is None

def test_clean_row_drops_missing_region():
    raw = dict(date="2024-01-01", product="X", category="Y", region="",
               quantity="5", unit_price="10", sales_rep="Alice", notes="")
    assert clean_row(raw, 0) is None

def test_clean_row_drops_missing_rep():
    raw = dict(date="2024-01-01", product="X", category="Y", region="West",
               quantity="5", unit_price="10", sales_rep="", notes="")
    assert clean_row(raw, 0) is None

def test_clean_row_normalizes_price():
    raw = dict(date="2024-01-01", product="X", category="Y", region="West",
               quantity="2", unit_price="$49.99", sales_rep="Alice", notes="")
    cleaned = clean_row(raw, 0)
    assert cleaned is not None
    assert cleaned["unit_price"] == 49.99

def test_clean_row_normalizes_rep_name():
    raw = dict(date="2024-01-01", product="X", category="Y", region="West",
               quantity="2", unit_price="10", sales_rep="bob smith", notes="")
    cleaned = clean_row(raw, 0)
    assert cleaned is not None
    assert cleaned["sales_rep"] == "Bob Smith"

def test_summarise_computes_totals():
    rows = [
        dict(category="A", region="West", sales_rep="Alice", revenue=100.0),
        dict(category="A", region="East", sales_rep="Bob", revenue=200.0),
        dict(category="B", region="West", sales_rep="Alice", revenue=50.0),
    ]
    s = summarise(rows)
    assert s["total"] == 350.0
    assert s["by_category"] == {"A": 300.0, "B": 50.0}
    assert s["by_region"] == {"West": 150.0, "East": 200.0}
    assert s["by_rep"] == {"Alice": 150.0, "Bob": 200.0}

def test_full_pipeline_drops_bad_rows():
    raw = read_raw(RAW)
    clean = [r for r in (clean_row(raw[i], i) for i in range(len(raw))) if r is not None]
    # Should drop: return row (-1 qty), missing region/rep row, zero qty row
    assert len(clean) == 16

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])