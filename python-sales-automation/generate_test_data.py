"""
Generates realistic but synthetic sales data in the "before" (messy) state.
Run this once to produce `sample_raw_sales.csv`.
"""

import csv
import random
from pathlib import Path

OUT = Path(__file__).parent / "sample_raw_sales.csv"

ROWS = [
    # (date, product, category, region, quantity, unit_price, sales_rep, notes)
    ("2024-01-05", "Widget Pro",      "Electronics",  "West",   3,  149.99, "Alice Novak",    "Customer requested bulk discount"),
    ("2024-01-07", "Gadget Basic",   "Electronics",  "East",   7,   49.99, "Bob Smith",      "Regular order"),
    ("2024-01-10", "Service Plan A", "Services",     "North",  1,  299.00, "Carol White",   "Annual subscription"),
    ("2024-01-12", "Widget Pro",     "Electronics",  "West",   -1, 149.99, "Alice Novak",   "RETURN"),
    ("2024-01-15", "Part X-100",     "Parts",        "South",  10,   9.99,  "Dave Lee",      ""),
    ("2024-01-18", "Gadget Basic",   "Electronics",  "East",   7,   49.99, "bob smith",      "regular order 2"),
    ("2024-01-22", "Service Plan B", "Services",     "North",  1,  199.00, "carol white",   ""),
    ("2024-01-25", "Widget Standard","Electronics",  "West",   5,   89.99, "Alice Novak",   ""),
    ("2024-01-28", "Part X-100",     "Parts",        "South",  20,   9.99,  "DAVE LEE",      "large order"),
    ("2024-02-01", "Gadget Basic",   "Electronics",  "East",   3,  "$54.99", "Bob Smith",   "price increase"),
    ("2024-02-04", "Service Plan A", "Services",     "Central",1,  299.00, "Eve Black",    ""),
    ("2024-02-08", "Widget Pro",     "Electronics",  "West",   4, 149.99,  "Alice Novak",   "  extra whitespace  "),
    ("2024-02-12", "Part Y-200",     "Parts",        "South",  8,  19.99,  "Dave Lee",     "N/A"),
    ("2024-02-15", "Gadget Basic",   "Electronics",  "East",   2,  "49.99", "bob smith",    "Repeat customer"),
    ("2024-02-20", "Service Plan C", "Services",     "North",  1,  499.00, "Carol White",  ""),
    ("2024-02-23", "Widget Standard","Electronics",  "Central",3,   89.99,  "Eve Black",    ""),
    # Intentional problems for the demo:
    ("2024-03-01", "Gadget Basic",   "Electronics",  "",       5,   49.99, "",              "Missing region & rep"),
    ("2024-03-05", "Unknown Item",   "Misc",         "West",   2,  100.00, "Bob Smith",    "Invalid product"),
    ("2024-03-10", "Widget Pro",     "Electronics",  "East",   0, 149.99, "Alice Novak",  "Zero qty — probably a data entry error"),
]

def write():
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "product", "category", "region", "quantity", "unit_price", "sales_rep", "notes"])
        for row in ROWS:
            writer.writerow(row)
    print(f"Written {OUT}")

if __name__ == "__main__":
    write()