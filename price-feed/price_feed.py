"""Price feed: supplier CSV -> clean product CSV with selling price (margin + VAT) and a list of problem rows."""
import csv
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

COLUMNS = ("kod", "nazev", "cena_bez_dph", "dph", "sklad")
OUT_COLUMNS = ("kod", "nazev", "cena_bez_dph", "dph", "prodejni_cena_s_dph", "sklad")


def parse_number(text: str) -> Decimal:
    text = text.replace("Kč", "").replace(" ", "").replace("\xa0", "")
    if not text:
        raise ValueError("prázdná hodnota")
    if "," in text:  # Czech format: 1.234,50 -> thousands dot, decimal comma
        text = text.replace(".", "").replace(",", ".")
    try:
        return Decimal(text)
    except InvalidOperation:
        raise ValueError(f"není číslo: {text!r}") from None


def selling_price(net: Decimal, vat: Decimal, margin: Decimal) -> int:
    """Net purchase price + margin %, plus VAT %, rounded to whole CZK."""
    price = net * (1 + margin / 100) * (1 + vat / 100)
    return int(price.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def convert(src: Path, margin: Decimal) -> tuple[list[dict], list[tuple[int, str]]]:
    """Columns (separator ;): kod, nazev, cena_bez_dph, dph, sklad. Returns (good rows, [(line, reason)])."""
    good, problems, seen = [], [], set()
    with open(src, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        missing = set(COLUMNS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Chybí sloupce: {', '.join(sorted(missing))}")
        for line, r in enumerate(reader, start=2):
            kod = (r["kod"] or "").strip()
            try:
                if not kod:
                    raise ValueError("chybí kód")
                if kod in seen:
                    raise ValueError(f"duplicitní kód {kod}")
                net, vat = parse_number(r["cena_bez_dph"]), parse_number(r["dph"])
                if net <= 0:
                    raise ValueError("cena musí být kladná")
                stock = max(int(parse_number(r["sklad"] or "0")), 0)  # negative stock -> 0
            except ValueError as e:
                problems.append((line, str(e)))
                continue
            seen.add(kod)
            good.append({"kod": kod, "nazev": r["nazev"].strip(), "cena_bez_dph": net, "dph": vat,
                         "prodejni_cena_s_dph": selling_price(net, vat, margin), "sklad": stock})
    return good, problems


def write(good: list[dict], problems: list[tuple[int, str]], out: Path) -> Path:
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLUMNS, delimiter=";")
        w.writeheader()
        w.writerows(good)
    bad = out.with_name(out.stem + "_problemy.csv")
    with open(bad, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["radek", "problem"])
        w.writerows(problems)
    return bad


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Použití: python price_feed.py dodavatel.csv vystup.csv [marze_procent]")
    g, p = convert(Path(sys.argv[1]), Decimal(sys.argv[3]) if len(sys.argv) > 3 else Decimal(25))
    write(g, p, Path(sys.argv[2]))
    print(f"Hotovo: {len(g)} produktů, {len(p)} problémových řádků.")
