# Invoice Watch (Hlídač faktur)

Python script: reads a CSV of invoices and creates an Excel file. Overdue invoices are red, invoices due within 7 days are orange. A second sheet lists who owes how much.

## Run
```
pip install openpyxl
python invoice_watch.py sample_faktury.csv faktury_prehled.xlsx
```
CSV columns (separator `;`): `cislo;odberatel;castka;splatnost;zaplaceno`. Dates `2026-10-24` or `24.10.2026`, amounts like `12 500,00`.

## Test
```
pip install pytest
python -m pytest
```
Sample data are made up. MIT license.
