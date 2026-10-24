# Price Feed (Převod ceníku dodavatele)

Python script: reads a supplier CSV, computes the selling price (purchase price + margin + VAT, rounded to whole CZK), sets negative stock to 0 and writes two files: a clean product CSV and a list of problem rows (missing code, duplicate code, price that is not a number).

## Run
```
python price_feed.py sample_dodavatel.csv vystup.csv 25
```
The last number is the margin in % (default 25). Output: `vystup.csv` and `vystup_problemy.csv`.
CSV columns (separator `;`): `kod;nazev;cena_bez_dph;dph;sklad`. Prices like `1 290,50` or `49,90 Kč` work.

## Test
```
pip install pytest
python -m pytest
```
Sample data are made up. The output columns are generic; it is not tied to any particular e-shop system. MIT license.
