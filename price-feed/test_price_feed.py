import csv
from decimal import Decimal
from pathlib import Path

import pytest

from price_feed import convert, parse_number, selling_price, write

SAMPLE = Path(__file__).parent / "sample_dodavatel.csv"


def test_parse_number():
    assert parse_number("1 290,50") == Decimal("1290.50")
    assert parse_number("49,90 Kč") == Decimal("49.90")
    with pytest.raises(ValueError):
        parse_number("abc")


def test_selling_price():
    # 100 + 25 % margin = 125, + 21 % VAT = 151.25 -> 151
    assert selling_price(Decimal(100), Decimal(21), Decimal(25)) == 151
    assert selling_price(Decimal(100), Decimal(21), Decimal(0)) == 121


def test_convert_good_rows():
    good, _ = convert(SAMPLE, Decimal(25))
    by_code = {r["kod"]: r for r in good}
    assert set(by_code) == {"KB-001", "KB-002", "KB-003", "KB-004", "KB-006"}
    assert by_code["KB-001"]["prodejni_cena_s_dph"] == 377  # 249 * 1.25 * 1.21 = 376.61
    assert by_code["KB-004"]["sklad"] == 0  # negative stock becomes 0
    assert by_code["KB-002"]["cena_bez_dph"] == Decimal("1290.50")  # first duplicate wins


def test_convert_problems():
    _, problems = convert(SAMPLE, Decimal(25))
    reasons = " | ".join(reason for _, reason in problems)
    assert len(problems) == 4
    assert "duplicitní kód KB-002" in reasons
    assert "chybí kód" in reasons
    assert "není číslo" in reasons


def test_missing_column(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("kod;nazev\nA;B\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Chybí sloupce"):
        convert(bad, Decimal(25))


def test_write_files(tmp_path):
    good, problems = convert(SAMPLE, Decimal(25))
    out = tmp_path / "vystup.csv"
    bad = write(good, problems, out)
    with open(out, newline="", encoding="utf-8-sig") as f:
        assert len(list(csv.DictReader(f, delimiter=";"))) == 5
    assert bad.name == "vystup_problemy.csv" and bad.is_file()
