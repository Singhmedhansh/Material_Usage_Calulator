#!/usr/bin/env python3
"""
Material Usage Calculator
A simple terminal-based application to track material usage with SQLite database.
"""

import sqlite3
import os
from datetime import datetime


class MaterialUsageCalculator:
    def __init__(self, db_name='material_usage.db'):
        """Initialize the calculator with database connection."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.setup_database()
    
    def setup_database(self):
        """Create database and tables if they don't exist."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # Create materials table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                unit TEXT NOT NULL,
                unit_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create usage table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                purpose TEXT,
                usage_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (material_id) REFERENCES materials (id)
            )
        ''')
        
        self.conn.commit()
    
    def add_material(self, name, unit, unit_price):
        """Add a new material to the database."""
        try:
            self.cursor.execute(
                'INSERT INTO materials (name, unit, unit_price) VALUES (?, ?, ?)',
                (name, unit, unit_price)
            )
            self.conn.commit()
            print(f"✓ Material '{name}' added successfully!")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Error: Material '{name}' already exists!")
            return False
        except Exception as e:
            print(f"✗ Error adding material: {e}")
            return False
    
    def record_usage(self, material_name, quantity, purpose=""):
        """Record material usage."""
        try:
            # Get material ID
            self.cursor.execute(
                'SELECT id FROM materials WHERE name = ?',
                (material_name,)
            )
            result = self.cursor.fetchone()
            
            if not result:
                print(f"✗ Error: Material '{material_name}' not found!")
                return False
            
            material_id = result[0]
            
            # Record usage
            self.cursor.execute(
                'INSERT INTO usage (material_id, quantity, purpose) VALUES (?, ?, ?)',
                (material_id, quantity, purpose)
            )
            self.conn.commit()
            print(f"✓ Usage recorded: {quantity} units of '{material_name}'")
            return True
        except Exception as e:
            print(f"✗ Error recording usage: {e}")
            return False
    
    def view_materials(self):
        """Display all materials."""
        self.cursor.execute('SELECT id, name, unit, unit_price FROM materials ORDER BY name')
        materials = self.cursor.fetchall()
        
        if not materials:
            print("\nNo materials found in the database.")
            return
        
        print("\n" + "="*70)
        print(f"{'ID':<5} {'Material Name':<25} {'Unit':<15} {'Unit Price':<15}")
        print("="*70)
        for material in materials:
            print(f"{material[0]:<5} {material[1]:<25} {material[2]:<15} ${material[3]:<14.2f}")
        print("="*70)
    
    def view_usage_history(self, material_name=None):
        """Display usage history, optionally filtered by material."""
        if material_name:
            query = '''
                SELECT u.id, m.name, u.quantity, m.unit, u.purpose, u.usage_date
                FROM usage u
                JOIN materials m ON u.material_id = m.id
                WHERE m.name = ?
                ORDER BY u.usage_date DESC
            '''
            self.cursor.execute(query, (material_name,))
        else:
            query = '''
                SELECT u.id, m.name, u.quantity, m.unit, u.purpose, u.usage_date
                FROM usage u
                JOIN materials m ON u.material_id = m.id
                ORDER BY u.usage_date DESC
            '''
            self.cursor.execute(query)
        
        usage_records = self.cursor.fetchall()
        
        if not usage_records:
            print("\nNo usage records found.")
            return
        
        print("\n" + "="*100)
        print(f"{'ID':<5} {'Material':<20} {'Quantity':<12} {'Unit':<10} {'Purpose':<30} {'Date':<20}")
        print("="*100)
        for record in usage_records:
            purpose = record[4] if record[4] else "N/A"
            print(f"{record[0]:<5} {record[1]:<20} {record[2]:<12.2f} {record[3]:<10} {purpose:<30} {record[5]:<20}")
        print("="*100)
    
    def calculate_total_usage(self):
        """Calculate and display total usage and cost for each material."""
        query = '''
            SELECT m.name, m.unit, m.unit_price, 
                   COALESCE(SUM(u.quantity), 0) as total_quantity,
                   COALESCE(SUM(u.quantity * m.unit_price), 0) as total_cost
            FROM materials m
            LEFT JOIN usage u ON m.id = u.material_id
            GROUP BY m.id, m.name, m.unit, m.unit_price
            ORDER BY m.name
        '''
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        if not results:
            print("\nNo materials found.")
            return
        
        print("\n" + "="*85)
        print(f"{'Material':<25} {'Unit':<12} {'Unit Price':<15} {'Total Used':<15} {'Total Cost':<15}")
        print("="*85)
        
        grand_total = 0
        for row in results:
            material_name, unit, unit_price, total_quantity, total_cost = row
            print(f"{material_name:<25} {unit:<12} ${unit_price:<14.2f} {total_quantity:<15.2f} ${total_cost:<14.2f}")
            grand_total += total_cost
        
        print("="*85)
        print(f"{'GRAND TOTAL':<68} ${grand_total:<14.2f}")
        print("="*85)
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print(" MATERIAL USAGE CALCULATOR ".center(50))
    print("="*50)
    print("1. Add Material")
    print("2. Record Material Usage")
    print("3. View All Materials")
    print("4. View Usage History")
    print("5. Calculate Total Usage & Cost")
    print("6. Exit")
    print("="*50)


def main():
    """Main function to run the calculator."""
    calculator = MaterialUsageCalculator()
    
    print("\n╔════════════════════════════════════════════════╗")
    print("║   Welcome to Material Usage Calculator!       ║")
    print("╚════════════════════════════════════════════════╝")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            # Add Material
            print("\n--- Add New Material ---")
            name = input("Enter material name: ").strip()
            if not name:
                print("✗ Material name cannot be empty!")
                continue
            
            unit = input("Enter unit (e.g., kg, liters, pieces): ").strip()
            if not unit:
                print("✗ Unit cannot be empty!")
                continue
            
            try:
                unit_price = float(input("Enter unit price: $").strip())
                if unit_price < 0:
                    print("✗ Price cannot be negative!")
                    continue
            except ValueError:
                print("✗ Invalid price! Please enter a number.")
                continue
            
            calculator.add_material(name, unit, unit_price)
        
        elif choice == '2':
            # Record Material Usage
            print("\n--- Record Material Usage ---")
            name = input("Enter material name: ").strip()
            if not name:
                print("✗ Material name cannot be empty!")
                continue
            
            try:
                quantity = float(input("Enter quantity used: ").strip())
                if quantity <= 0:
                    print("✗ Quantity must be positive!")
                    continue
            except ValueError:
                print("✗ Invalid quantity! Please enter a number.")
                continue
            
            purpose = input("Enter purpose (optional): ").strip()
            calculator.record_usage(name, quantity, purpose)
        
        elif choice == '3':
            # View All Materials
            print("\n--- All Materials ---")
            calculator.view_materials()
        
        elif choice == '4':
            # View Usage History
            print("\n--- Usage History ---")
            filter_choice = input("Filter by material? (y/n): ").strip().lower()
            
            if filter_choice == 'y':
                name = input("Enter material name: ").strip()
                calculator.view_usage_history(name)
            else:
                calculator.view_usage_history()
        
        elif choice == '5':
            # Calculate Total Usage
            print("\n--- Total Usage & Cost Summary ---")
            calculator.calculate_total_usage()
        
        elif choice == '6':
            # Exit
            print("\nThank you for using Material Usage Calculator!")
            print("Goodbye! 👋\n")
            calculator.close()
            break
        
        else:
            print("✗ Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
