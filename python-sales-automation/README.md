# Python Sales Automation Demo

Clean raw CSV sales data automatically — drops bad rows, normalises
names and prices, computes KPI summaries, and renders a bar chart.

## Before vs After

| Step | Before | After |
|------|--------|-------|
| Raw CSV | 19 rows: mixed-case names, currency symbols, negative/zero quantities, missing regions | 16 clean rows, `$`-prefixes stripped, Title Case reps |
| Revenue column | absent — you calculate it manually | `revenue = quantity x unit_price` for every row |
| Invalid rows | present (returns, data-entry errors, blank fields) | silently dropped and counted in the report |
| Report | manually copy-paste into a spreadsheet | printed to stdout + a clean CSV written to disk |
| Chart | nonexistent | `sales_figure.png` — revenue by category |

## Quick start

```bash
# 1. Generate test data (one-time)
python generate_test_data.py

# 2. Run the cleaner
python main.py

# 3. Inspect the output
cat clean_sales_report.csv
```

## Sample output

```
=======================================================
  SALES REPORT SUMMARY
=======================================================
  Raw rows read   : 19
  Valid rows kept : 16
  Rows dropped    : 3  (15.8%)
  Total revenue   : $5,149.30

  Category          Revenue
  ----------------------------
  Electronics         $1,899.30
  Services            $1,296.00
  Parts                 $409.80
  Misc                  $200.00
=======================================================
```

## Cleaning rules applied

- Quantity <= 0 → row dropped (returns, data-entry errors)
- Missing region or sales_rep → row dropped
- Price strings → `$`, `€`, `£`, commas and spaces stripped, converted to float
- Rep names → Title Case normalised (`bob smith` → `Bob Smith`)
- Whitespace → stripped from all text fields

## Running tests

```bash
pip install pytest matplotlib
pytest test_main.py -v
```

Expected result: **9 tests pass**.

## Dependencies

- matplotlib (chart rendering)
- pytest (tests)
- Standard library: csv, re, collections, pathlib

## Project structure

```
python-sales-automation/
├── main.py                  # run this
├── generate_test_data.py   # creates sample_raw_sales.csv
├── test_main.py            # pytest suite (9 tests)
├── sample_raw_sales.csv    # generated input (19 messy rows)
├── clean_sales_report.csv  # generated output
└── sales_figure.png        # generated chart
```
