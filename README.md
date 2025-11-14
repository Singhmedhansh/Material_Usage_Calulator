# Material Usage Calculator

A simple terminal-based Material Usage Calculator built with Python and SQLite. This application allows you to track materials, record their usage, and calculate total costs - all from the command line.

## Features

- ✅ Add materials with name, unit, and unit price
- ✅ Record material usage with quantity and purpose
- ✅ View all materials in inventory
- ✅ View complete usage history (with optional filtering)
- ✅ Calculate total usage and cost for all materials
- ✅ SQLite database for persistent storage
- ✅ Terminal-based interface (no GUI)

## Requirements

- Python 3.6 or higher
- SQLite3 (included with Python)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Singhmedhansh/Material_Usage_Calulator.git
cd Material_Usage_Calulator
```

2. No additional dependencies needed! SQLite comes built-in with Python.

## Usage

Run the calculator from the terminal:

```bash
python3 material_calculator.py
```

### Main Menu Options

1. **Add Material**: Add a new material to the database
   - Enter material name
   - Enter unit (e.g., kg, liters, pieces)
   - Enter unit price

2. **Record Material Usage**: Record when you use a material
   - Enter material name
   - Enter quantity used
   - Enter purpose (optional)

3. **View All Materials**: Display all materials in the database

4. **View Usage History**: Display usage records
   - Option to filter by specific material

5. **Calculate Total Usage & Cost**: View summary of total usage and costs for all materials

6. **Exit**: Exit the application

## Example Usage

```
=================================================
         MATERIAL USAGE CALCULATOR
=================================================
1. Add Material
2. Record Material Usage
3. View All Materials
4. View Usage History
5. Calculate Total Usage & Cost
6. Exit
=================================================

Enter your choice (1-6): 1

--- Add New Material ---
Enter material name: Cement
Enter unit (e.g., kg, liters, pieces): kg
Enter unit price: $5.50
✓ Material 'Cement' added successfully!
```

## Database

The application creates a SQLite database file `material_usage.db` in the same directory. This file contains:

### Tables

- **materials**: Stores material information (id, name, unit, unit_price, created_at)
- **usage**: Stores usage records (id, material_id, quantity, purpose, usage_date)

## License

This project is open source and available for personal and educational use.

## Author

Singhmedhansh