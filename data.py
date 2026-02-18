"""
data.py — CSV storage for transaction history (history.csv).

Columns:
  Timestamp, Category, Material, Quantity, Total_Cost

Uses the builtin csv module.
"""

import csv
from pathlib import Path

CSV_FILE = Path("history.csv")
CSV_FIELDS = ["Timestamp", "Category", "Material", "Quantity", "Total_Cost"]


def _ensure_csv_exists():
    """
    Create the CSV with header if it does not exist.
    """
    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def save_transaction(timestamp: str, category: str, material: str, quantity: str, total_cost: str):
    """
    Appends a row to history.csv. quantity and total_cost should be strings.
    """
    _ensure_csv_exists()
    with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow({
            "Timestamp": timestamp,
            "Category": category,
            "Material": material,
            "Quantity": quantity,
            "Total_Cost": total_cost
        })


def view_history():
    """
    Reads history.csv and prints a nicely formatted table to console.
    """
    _ensure_csv_exists()
    rows = []
    with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("No transactions yet.")
        return

    # determine column widths
    cols = CSV_FIELDS
    widths = {c: len(c) for c in cols}
    for r in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(r.get(c, ""))))

    # header
    header = " | ".join(f"{c:{widths[c]}}" for c in cols)
    sep = "-+-".join("-" * widths[c] for c in cols)
    print(header)
    print(sep)
    # rows
    for r in rows:
        line = " | ".join(f"{str(r.get(c,'')):{widths[c]}}" for c in cols)
        print(line)


def clear_history():
    """
    Clears all transaction rows from history.csv while keeping the header.
    """
    with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
