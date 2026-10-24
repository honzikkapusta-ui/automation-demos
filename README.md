# Automation Demos — Python & Excel for Small Business

**EN** | [ČESKY](#česky)

---

## English

Four local demonstrations using synthetic data: CSV cleanup, a generated Excel report, an invoice-due tracker and a supplier price list converter. They are examples for review, not completed customer integrations.

### 📦 What's Inside

| Demo | Description | Tests | Output |
|------|-------------|-------|--------|
| **python-sales-automation** | Reads messy CSV (mixed case, $ prefixes, negative/zero qty, missing fields) → cleans → writes clean CSV + revenue column + KPI summary + bar chart | 9 passing | `clean_sales_report.csv`, `sales_figure.png` |
| **excel-report-builder** | Creates professional multi-sheet workbook with formulas, pivot tables (SUMIFS/COUNTIFS), KPI dashboard, embedded chart | 7 passing | `monthly_sales_report.xlsx` (3 sheets) |
| **invoice-watch** | Reads a CSV of invoices → Excel with overdue (red) and due-soon (orange) rows + a debtors sheet | 6 passing | `faktury_prehled.xlsx` |
| **price-feed** | Reads a supplier price list CSV → computes the selling price (margin + VAT), fixes negative stock, writes a clean CSV plus a list of problem rows (missing/duplicate code, invalid price) | 6 passing | `vystup.csv`, `vystup_problemy.csv` |

### 🚀 Quick Start

```bash
# Demo 1: Python Sales Automation
cd python-sales-automation
python generate_test_data.py   # creates sample_raw_sales.csv
python main.py                 # produces clean_sales_report.csv + sales_figure.png
pytest test_main.py -v         # 9 tests pass

# Demo 2: Excel Report Builder
cd ../excel-report-builder
pip install openpyxl
python excel_builder.py        # produces monthly_sales_report.xlsx
pytest test_excel_builder.py -v # 7 tests pass

# Demo 3: Invoice Watch
cd ../invoice-watch
python invoice_watch.py sample_faktury.csv faktury_prehled.xlsx
pytest -v                      # 6 tests pass

# Demo 4: Price Feed
cd ../price-feed
python price_feed.py sample_dodavatel.csv vystup.csv 25   # 25 = margin in %
pytest -v                      # 6 tests pass
```

### 🎯 Use Cases

- **Supplied tabular exports**: CSV cleanup demonstrated on synthetic sales data.
- **Excel report**: Data, category summaries and a dashboard/chart; formula results require verification in the target spreadsheet application.
- **Additional integrations**: Shoptet, accounting imports, advertising APIs, PDF/OCR and unattended scheduling are not validated by these demos. Each requires separate scope and testing.

### 🛠 Stack

Python • pandas • openpyxl • matplotlib • pytest. A workflow file is included; successful hosted CI or unattended operation is not claimed.

### 📄 License

MIT — free to use, modify, distribute. Attribution appreciated.

### Portfolio

https://honzikkapusta-ui.github.io/automation-demos/

---

## ČESKY

Čtyři lokální ukázky na syntetických datech: čištění CSV, generovaný Excel report, hlídač splatnosti faktur a převod ceníku dodavatele. Nejde o dokončené integrace pro klienty.

### 📦 Co uvnitř

| Demo | Popis | Testy | Výstup |
|------|-------|-------|--------|
| **python-sales-automation** | Načte chaotické CSV (míchané velikosti písmen, $ u cen, záporná/nulová množství, chybějící pole) → vyčistí → zapíše čisté CSV + sloupec revenue + KPI souhrn + sloupcový graf | 9 prochází | `clean_sales_report.csv`, `sales_figure.png` |
| **excel-report-builder** | Vytvoří profesionální vícelistovou Excel s vzorci, pivot tabulkami (SUMIFS/COUNTIFS), KPI dashboardem, vloženým grafem | 7 prochází | `monthly_sales_report.xlsx` (3 listy) |
| **invoice-watch** | Načte CSV s fakturami → Excel s fakturami po splatnosti (červeně), brzy splatnými (oranžově) a listem dlužníků | 6 prochází | `faktury_prehled.xlsx` |
| **price-feed** | Načte CSV s ceníkem dodavatele → spočítá prodejní cenu (marže + DPH), opraví záporný sklad, zapíše čisté CSV a seznam problémových řádků (chybí/duplicitní kód, neplatná cena) | 6 prochází | `vystup.csv`, `vystup_problemy.csv` |

### 🚀 Rychlý start

```bash
# Demo 1: Python Sales Automation
cd python-sales-automation
python generate_test_data.py   # vytvoří sample_raw_sales.csv
python main.py                 # vyprodukuje clean_sales_report.csv + sales_figure.png
pytest test_main.py -v         # 9 testů projde

# Demo 2: Excel Report Builder
cd ../excel-report-builder
pip install openpyxl
python excel_builder.py        # vyprodukuje monthly_sales_report.xlsx
pytest test_excel_builder.py -v # 7 testů projde

# Demo 3: Invoice Watch
cd ../invoice-watch
python invoice_watch.py sample_faktury.csv faktury_prehled.xlsx
pytest -v                      # 6 testů projde

# Demo 4: Price Feed
cd ../price-feed
python price_feed.py sample_dodavatel.csv vystup.csv 25   # 25 = marže v %
pytest -v                      # 6 testů projde
```

### 🎯 Případy užití

- **Dodané tabulkové exporty**: Čištění CSV a ukázkový prodejní report ze syntetických dat.
- **Excel report**: Datový list, souhrny kategorií a přehled s grafem. Výpočty musí ověřit cílová tabulková aplikace.
- **Další integrace**: Shoptet, účetní systémy, reklamní API, PDF/OCR a automatické plánování nejsou těmito demy ověřené dodávky. Vyžadují samostatné zadání a validaci.

### 🛠 Stack

Python • pandas • openpyxl • matplotlib • pytest. Přiložený workflow není důkazem úspěšného hostovaného CI ani bezobslužného provozu.

### 📄 Licence

MIT — volné použití, úpravy, šíření. Úžasné, když uveďte zdroj.

### 🔗 Živé portfolio

https://honzikkapusta-ui.github.io/automation-demos/

---

## Contact / Kontakt

**Honza Kapusta** — Python automation & Excel reporting for small businesses  
**Email**: honzikkapusta@seznam.cz • **GitHub**: [https://github.com/honzikkapusta-ui](https://github.com/honzikkapusta-ui)

