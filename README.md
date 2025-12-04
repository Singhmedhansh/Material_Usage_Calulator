# Material Usage Calculator

Simple terminal-based Material Usage Calculator for construction and household renovation tasks. This project is a college assignment scaffold for calculating materials, estimating costs and saving transactions.

## Files
- `main.py` — entrypoint and interactive menu (Construction, Household, History).
- `calculations.py` — all math formulas for bricks, cement, sand, paint and flooring.
- `storage.py` — CSV-based storage for transactions (`project_data.csv`).
- `utils.py` — input validation helpers to avoid crashes.

## Quick start

Prerequisites: Python 3.8+ (no external libraries required).

Run from the project root:

```powershell
python main.py
```

Follow the on-screen prompts. When you calculate a cost, the transaction is saved to `project_data.csv`.

## Transaction CSV
- `project_data.csv` columns: `Timestamp, Category, Material, Quantity, Total_Cost`.
- Use the "View Transaction History" menu option to inspect saved transactions.

## Team
- Team Member 1: Name
- Team Member 2: Name
- Team Member 3: Name
- Team Member 4: Name

Replace the placeholder names with your team members' names.

## Development notes
- The calculations are implemented in `calculations.py` and should be covered by unit tests (not included).
- To add tests, create a `tests/` folder and use `pytest` or `unittest`.

## License
Add a license file if you plan to publish this repository.
