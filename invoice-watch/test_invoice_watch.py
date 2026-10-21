from datetime import date
from pathlib import Path

from openpyxl import load_workbook

from invoice_watch import build, load, parse_amount, parse_date, status

SAMPLE = Path(__file__).parent / "sample_faktury.csv"
TODAY = date(2026, 10, 21)


def test_parsing():
    assert parse_amount("12 500,00") == 12500.0
    assert parse_date("24.10.2026") == date(2026, 10, 24) == parse_date("2026-10-24")


def test_status():
    by_no = {r["cislo"]: status(r, TODAY) for r in load(SAMPLE)}
    assert by_no["2026001"] == "po splatnosti"
    assert by_no["2026003"] == "zaplaceno"
    assert by_no["2026005"] == "brzy splatné"
    assert by_no["2026007"] == "v pořádku"


def test_output(tmp_path):
    res = build(load(SAMPLE), tmp_path / "o.xlsx", TODAY)
    assert res["po_splatnosti"] == 12500 + 4200 + 7300 + 15000
    wb = load_workbook(tmp_path / "o.xlsx")
    assert wb["Dlužníci"]["A2"].value == "Novák Instalatérství"  # biggest debtor first
    assert wb["Dlužníci"].cell(wb["Dlužníci"].max_row, 2).value == res["po_splatnosti"]
