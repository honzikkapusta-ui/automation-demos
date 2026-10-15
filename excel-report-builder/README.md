# Excel Report Builder Demo

Creates a professional multi-sheet Excel workbook with formulas, pivot tables,
and an embedded chart — all from Python. No VBA, no manual formatting.

## Before vs After

| Task | Manual / VBA | Python (this demo) |
|------|--------------|-------------------|
| Data entry | Typing or copy-paste | Data generated / imported from CSV |
| Revenue column | Type `=E2*F2` and drag down | Formula written programmatically |
| Category summary | PivotTable wizard, drag fields | `SUMIFS` / `COUNTIFS` formulas |
| KPI dashboard | Manual layout, hard-coded numbers | Live formulas referencing data sheet |
| Chart | Insert > Chart, format manually | `openpyxl.chart.BarChart` embedded |
| Re-run next month | Repeat all steps | Re-run script with new data |

## Quick start

```bash
pip install openpyxl
python excel_builder.py
```

Opens `monthly_sales_report.xlsx` with three sheets:

1. **Sales Data** — raw table with auto-filter, revenue formula in column G
2. **By Category** — pivot formulas (SUMIFS/COUNTIFS), totals row
3. **Dashboard** — KPI cards (Total Revenue, Orders, Avg Order, Top Category) + bar chart

## Sample output

The Dashboard sheet contains live formulas:
- Total Revenue: `=SUM('Sales Data'!G:G)`
- Total Orders: `=COUNTA('Sales Data'!A:A)-1`
- Avg Order Value: `=IFERROR(B2/B3,0)` (revenue divided by order count; zero when empty)
- Top Category: `=INDEX(... MATCH(MAX(...)))`

The bar chart is embedded. Formula values and chart rendering must be checked in the target spreadsheet application; Python writes formulas without evaluating them. The script currently uses embedded synthetic data, not a general CSV import interface. Category summaries use SUMIFS/COUNTIFS, not native Excel PivotTable objects.

## Running tests

```bash
pip install pytest openpyxl
pytest test_excel_builder.py -v
```

All 7 tests should pass.

## Dependencies

- `openpyxl` (reading/writing .xlsx)
- `pytest` (tests)

## Project structure

```
excel-report-builder/
├── excel_builder.py         # run this
├── test_excel_builder.py    # pytest suite
└── monthly_sales_report.xlsx  # generated output
```
