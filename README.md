# Material Usage Calculator

A Python CLI application for tracking material inventory and usage with persistent SQLite storage.

## Features

- **Material Management**: Add, update, delete, and view materials with unit prices
- **Usage Tracking**: Record material usage with quantity, purpose, and timestamp
- **Inventory Overview**: View comprehensive inventory summary with total usage and costs
- **Usage History**: Filter and view usage records by material or purpose
- **Cost Calculations**: Automatic cost calculation with aggregation by material or total
- **Persistent Storage**: All data stored in SQLite database

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Singhmedhansh/Material_Usage_Calulator.git
cd Material_Usage_Calulator
```

2. Make the script executable (optional):
```bash
chmod +x material_calculator.py
```

## Usage

### Running the Application

```bash
python3 material_calculator.py
```

### Menu Options

1. **Material Management**
   - Add new materials with name, unit, and unit price
   - View all materials in inventory
   - Update existing material details
   - Delete materials (including their usage records)

2. **Record Usage**
   - Select a material from inventory
   - Enter quantity used
   - Optionally add purpose/description

3. **View Inventory**
   - See all materials with their total usage and costs
   - View grand total cost across all materials

4. **View Usage History**
   - View all usage records chronologically
   - Filter by specific material
   - Filter by purpose keyword

5. **Calculate Costs**
   - View total cost across all materials
   - View cost breakdown by individual material

## Database Schema

### Materials Table
- `id`: Primary key (auto-increment)
- `name`: Material name (unique)
- `unit`: Unit of measurement (e.g., kg, liters, pieces)
- `unit_price`: Price per unit

### Usage Table
- `id`: Primary key (auto-increment)
- `material_id`: Foreign key to materials table
- `quantity`: Amount used
- `purpose`: Description of usage (optional)
- `timestamp`: ISO format timestamp of when usage was recorded

## Running Tests

The project includes comprehensive unit tests covering all functionality:

```bash
python3 -m unittest test_calculator.py -v
```

Test coverage includes:
- Database setup and schema validation
- CRUD operations for materials
- Usage recording and retrieval
- Cost calculations and aggregations
- Edge cases and error handling

## Example Usage

```python
from material_calculator import MaterialCalculator

# Initialize calculator
calc = MaterialCalculator("my_materials.db")

# Add materials
calc.add_material("Steel", "kg", 5.50)
calc.add_material("Cement", "bags", 12.00)

# Record usage
steel = calc.get_material_by_name("Steel")
calc.record_usage(steel['id'], 100.5, "Construction project")

# Calculate costs
total_cost = calc.calculate_total_cost()
print(f"Total cost: ${total_cost:.2f}")

# Close connection
calc.close()
```

## File Structure

```
.
├── .gitignore              # Excludes database files and Python artifacts
├── material_calculator.py  # Main application with CLI interface
├── test_calculator.py      # Comprehensive unit test suite
└── README.md              # This file
```

## License

This project is open source and available under the MIT License.