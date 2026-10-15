"""Sales Report Automation — reads messy CSV, cleans it, outputs a clean CSV + chart."""
import csv, re, sys
from collections import defaultdict
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_IN  = Path(__file__).parent / "sample_raw_sales.csv"
CSV_OUT = Path(__file__).parent / "clean_sales_report.csv"
CHART   = Path(__file__).parent / "sales_figure.png"

def read_raw(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def clean_row(raw, idx):
    qty   = _parse_float(raw["quantity"])
    price = _parse_price(raw["unit_price"])
    if qty is None or qty <= 0: return None
    if not raw["region"].strip() or not raw["sales_rep"].strip(): return None
    return dict(
        date=raw["date"].strip(), product=raw["product"].strip(),
        category=raw["category"].strip(), region=raw["region"].strip(),
        quantity=float(qty), unit_price=float(price),
        revenue=round(qty * price, 2),
        sales_rep=raw["sales_rep"].strip().title(), notes=raw["notes"].strip(),
    )

def _parse_float(s):
    try: return float(s.strip())
    except ValueError: return None

def _parse_price(s):
    return _parse_float(re.sub(r"[$€£,\s]", "", s.strip()))

def write_clean(rows, path):
    FIELDS = ["date","product","category","region","quantity","unit_price","revenue","sales_rep","notes"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print(f"Clean CSV -> {path}")

def summarise(rows):
    by_cat = defaultdict(float); by_reg = defaultdict(float); by_rep = defaultdict(float)
    for r in rows:
        by_cat[r["category"]] += r["revenue"]
        by_reg[r["region"]]   += r["revenue"]
        by_rep[r["sales_rep"]] += r["revenue"]
    total = sum(r["revenue"] for r in rows)
    return dict(total=round(total,2), orders=len(rows),
                by_category=dict(sorted(by_cat.items(), key=lambda x:-x[1])),
                by_region=dict(sorted(by_reg.items(), key=lambda x:-x[1])),
                by_rep=dict(sorted(by_rep.items(), key=lambda x:-x[1])))

def render_chart(summary, out):
    cats = list(summary["by_category"].keys()); vals = list(summary["by_category"].values())
    fig, ax = plt.subplots(figsize=(8,4), dpi=120)
    bars = ax.bar(cats, vals, color=["#4F46E5","#10B981","#F59E0B","#EF4444","#8B5CF6"])
    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+5, f"${b.get_height():,.0f}",
                ha="center", va="bottom", fontsize=9)
    ax.set_title("Revenue by Category", fontsize=13, fontweight="bold")
    ax.set_ylabel("Revenue ($)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"${x:,.0f}"))
    fig.tight_layout(); fig.savefig(out); plt.close()
    print(f"Chart -> {out}")

def print_report(summary, n_in, n_out):
    print("\n" + "="*55)
    print("  SALES REPORT SUMMARY")
    print("="*55)
    print(f"  Raw rows read   : {n_in}")
    print(f"  Valid rows kept : {n_out}")
    print(f"  Rows dropped    : {n_in - n_out}  ({100*(n_in-n_out)/n_in:.1f}%)")
    print(f"  Total revenue   : ${summary['total']:,.2f}")
    print()
    print(f"  {'Category':<15} {'Revenue':>12}")
    print(f"  {'-'*28}")
    for c, v in summary["by_category"].items():
        print(f"  {c:<15} ${v:>11,.2f}")
    print("="*55+"\n")

def main():
    if not CSV_IN.exists():
        print(f"Error: {CSV_IN} not found — run generate_test_data.py first.", file=sys.stderr)
        return 1
    raw_rows = read_raw(CSV_IN)
    clean_rows = [r for r in (clean_row(raw_rows[i], i) for i in range(len(raw_rows))) if r is not None]
    summary = summarise(clean_rows)
    write_clean(clean_rows, CSV_OUT)
    render_chart(summary, CHART)
    print_report(summary, len(raw_rows), len(clean_rows))
    return 0

if __name__ == "__main__": sys.exit(main())