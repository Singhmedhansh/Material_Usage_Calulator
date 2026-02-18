# Material Usage Calculator

Terminal-based calculator for construction and household renovation estimates.
It calculates material quantities, supports optional cost estimation, and stores
transactions in CSV format.

## Current project files
- `main.py` — app entry point and menu flow.
- `calc.py` — all formulas (bricks, cement/sand, paint, flooring).
- `check.py` — input validation helpers.
- `data.py` — CSV storage helpers.
- `history.csv` — saved transaction history.
- `sample inputs/` — sample assets/files.

## Features
- Construction mode: bricks, cement bags, and sand (cu ft).
- Household mode: paint and flooring tile calculations.
- Optional cost calculation after each estimate.
- View and clear transaction history from the menu.

## Quick start
Prerequisites: Python 3.8+ (no external dependencies).

Run from project root:

```powershell
python main.py
```

## Transaction file
All saved records are written to `history.csv` with columns:

`Timestamp, Category, Material, Quantity, Total_Cost`

Use **View Transaction History** in the app menu to display saved records.

## Team Members
- Medhansh Pratap Singh — USN: RVCE25BAI015
- Ishan Jain — USN: RVCE25BAI184
- Namya K M — USN: RVCE25BAI175
- Medha Swetha Muguda — USN: RVCE25BAI072
