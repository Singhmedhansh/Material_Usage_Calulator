#!/usr/bin/env python3
"""
Material Usage Calculator - CLI application for tracking material inventory and usage
"""
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple
import sys


class MaterialCalculator:
    """Main class for managing materials and usage tracking"""
    
    def __init__(self, db_name: str = "materials.db"):
        """Initialize the calculator with a database connection"""
        self.db_name = db_name
        self.conn = None
        self.setup_database()
    
    def setup_database(self):
        """Create database connection and tables if they don't exist"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            
            # Create materials table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    unit TEXT NOT NULL,
                    unit_price REAL NOT NULL
                )
            """)
            
            # Create usage table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    material_id INTEGER NOT NULL,
                    quantity REAL NOT NULL,
                    purpose TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (material_id) REFERENCES materials (id)
                )
            """)
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            sys.exit(1)
    
    def add_material(self, name: str, unit: str, unit_price: float) -> bool:
        """Add a new material to the inventory"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO materials (name, unit, unit_price) VALUES (?, ?, ?)",
                (name, unit, unit_price)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Material '{name}' already exists.")
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_all_materials(self) -> List[sqlite3.Row]:
        """Get all materials from inventory"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM materials ORDER BY name")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_material_by_id(self, material_id: int) -> Optional[sqlite3.Row]:
        """Get a specific material by ID"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM materials WHERE id = ?", (material_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def get_material_by_name(self, name: str) -> Optional[sqlite3.Row]:
        """Get a specific material by name"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM materials WHERE name = ?", (name,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def update_material(self, material_id: int, name: str, unit: str, unit_price: float) -> bool:
        """Update an existing material"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE materials SET name = ?, unit = ?, unit_price = ? WHERE id = ?",
                (name, unit, unit_price, material_id)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print(f"Error: Material name '{name}' already exists.")
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def delete_material(self, material_id: int) -> bool:
        """Delete a material and its usage records"""
        try:
            cursor = self.conn.cursor()
            # Delete usage records first
            cursor.execute("DELETE FROM usage WHERE material_id = ?", (material_id,))
            # Delete material
            cursor.execute("DELETE FROM materials WHERE id = ?", (material_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def record_usage(self, material_id: int, quantity: float, purpose: str = "") -> bool:
        """Record usage of a material"""
        try:
            cursor = self.conn.cursor()
            timestamp = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO usage (material_id, quantity, purpose, timestamp) VALUES (?, ?, ?, ?)",
                (material_id, quantity, purpose, timestamp)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_all_usage(self) -> List[sqlite3.Row]:
        """Get all usage records with material details"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT u.id, u.material_id, m.name, m.unit, u.quantity, 
                       u.purpose, u.timestamp, m.unit_price
                FROM usage u
                JOIN materials m ON u.material_id = m.id
                ORDER BY u.timestamp DESC
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_usage_by_material(self, material_id: int) -> List[sqlite3.Row]:
        """Get usage records for a specific material"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT u.id, u.material_id, m.name, m.unit, u.quantity, 
                       u.purpose, u.timestamp, m.unit_price
                FROM usage u
                JOIN materials m ON u.material_id = m.id
                WHERE u.material_id = ?
                ORDER BY u.timestamp DESC
            """, (material_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def get_usage_by_purpose(self, purpose: str) -> List[sqlite3.Row]:
        """Get usage records filtered by purpose"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT u.id, u.material_id, m.name, m.unit, u.quantity, 
                       u.purpose, u.timestamp, m.unit_price
                FROM usage u
                JOIN materials m ON u.material_id = m.id
                WHERE u.purpose LIKE ?
                ORDER BY u.timestamp DESC
            """, (f"%{purpose}%",))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def calculate_total_cost(self, material_id: Optional[int] = None) -> float:
        """Calculate total cost of material usage"""
        try:
            cursor = self.conn.cursor()
            if material_id:
                cursor.execute("""
                    SELECT SUM(u.quantity * m.unit_price) as total
                    FROM usage u
                    JOIN materials m ON u.material_id = m.id
                    WHERE u.material_id = ?
                """, (material_id,))
            else:
                cursor.execute("""
                    SELECT SUM(u.quantity * m.unit_price) as total
                    FROM usage u
                    JOIN materials m ON u.material_id = m.id
                """)
            result = cursor.fetchone()
            return result['total'] if result['total'] is not None else 0.0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0.0
    
    def get_material_summary(self) -> List[Tuple]:
        """Get summary of total usage and cost per material"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.id, m.name, m.unit, m.unit_price,
                       COALESCE(SUM(u.quantity), 0) as total_quantity,
                       COALESCE(SUM(u.quantity * m.unit_price), 0) as total_cost
                FROM materials m
                LEFT JOIN usage u ON m.id = u.material_id
                GROUP BY m.id, m.name, m.unit, m.unit_price
                ORDER BY m.name
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class MaterialCalculatorUI:
    """Terminal UI for the Material Calculator"""
    
    def __init__(self):
        """Initialize the UI with a calculator instance"""
        self.calculator = MaterialCalculator()
    
    def clear_screen(self):
        """Clear the terminal screen"""
        print("\n" * 2)
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_materials_table(self, materials: List[sqlite3.Row]):
        """Print materials in a formatted table"""
        if not materials:
            print("\nNo materials found.")
            return
        
        print("\n{:<5} {:<25} {:<15} {:<15}".format("ID", "Name", "Unit", "Unit Price"))
        print("-" * 60)
        for material in materials:
            print("{:<5} {:<25} {:<15} ${:<14.2f}".format(
                material['id'], material['name'], material['unit'], material['unit_price']
            ))
    
    def print_usage_table(self, usage_records: List[sqlite3.Row]):
        """Print usage records in a formatted table"""
        if not usage_records:
            print("\nNo usage records found.")
            return
        
        print("\n{:<5} {:<20} {:<10} {:<20} {:<20}".format(
            "ID", "Material", "Quantity", "Purpose", "Date"
        ))
        print("-" * 80)
        for record in usage_records:
            # Format timestamp
            try:
                dt = datetime.fromisoformat(record['timestamp'])
                date_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = record['timestamp'][:16]
            
            purpose = record['purpose'] if record['purpose'] else "N/A"
            quantity_str = f"{record['quantity']} {record['unit']}"
            
            print("{:<5} {:<20} {:<10} {:<20} {:<20}".format(
                record['id'], record['name'][:20], quantity_str[:10], 
                purpose[:20], date_str
            ))
    
    def display_main_menu(self):
        """Display the main menu"""
        self.print_header("Material Usage Calculator")
        print("\n1. Material Management")
        print("2. Record Usage")
        print("3. View Inventory")
        print("4. View Usage History")
        print("5. Calculate Costs")
        print("6. Exit")
        print()
    
    def material_management_menu(self):
        """Handle material management operations"""
        while True:
            self.print_header("Material Management")
            print("\n1. Add Material")
            print("2. View All Materials")
            print("3. Update Material")
            print("4. Delete Material")
            print("5. Back to Main Menu")
            print()
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                self.add_material()
            elif choice == '2':
                self.view_all_materials()
            elif choice == '3':
                self.update_material()
            elif choice == '4':
                self.delete_material()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_material(self):
        """Add a new material"""
        self.print_header("Add Material")
        
        name = input("\nEnter material name: ").strip()
        if not name:
            print("Error: Material name cannot be empty.")
            return
        
        unit = input("Enter unit (e.g., kg, liters, pieces): ").strip()
        if not unit:
            print("Error: Unit cannot be empty.")
            return
        
        try:
            unit_price = float(input("Enter unit price ($): ").strip())
            if unit_price < 0:
                print("Error: Unit price cannot be negative.")
                return
        except ValueError:
            print("Error: Invalid price format.")
            return
        
        if self.calculator.add_material(name, unit, unit_price):
            print(f"\n✓ Material '{name}' added successfully!")
        else:
            print(f"\n✗ Failed to add material.")
    
    def view_all_materials(self):
        """View all materials"""
        self.print_header("All Materials")
        materials = self.calculator.get_all_materials()
        self.print_materials_table(materials)
        input("\nPress Enter to continue...")
    
    def update_material(self):
        """Update an existing material"""
        self.print_header("Update Material")
        
        materials = self.calculator.get_all_materials()
        self.print_materials_table(materials)
        
        if not materials:
            return
        
        try:
            material_id = int(input("\nEnter material ID to update: ").strip())
        except ValueError:
            print("Error: Invalid ID format.")
            return
        
        material = self.calculator.get_material_by_id(material_id)
        if not material:
            print(f"Error: Material with ID {material_id} not found.")
            return
        
        print(f"\nCurrent values: {material['name']}, {material['unit']}, ${material['unit_price']:.2f}")
        
        name = input("Enter new name (or press Enter to keep current): ").strip()
        name = name if name else material['name']
        
        unit = input("Enter new unit (or press Enter to keep current): ").strip()
        unit = unit if unit else material['unit']
        
        price_input = input("Enter new price (or press Enter to keep current): ").strip()
        if price_input:
            try:
                unit_price = float(price_input)
                if unit_price < 0:
                    print("Error: Unit price cannot be negative.")
                    return
            except ValueError:
                print("Error: Invalid price format.")
                return
        else:
            unit_price = material['unit_price']
        
        if self.calculator.update_material(material_id, name, unit, unit_price):
            print(f"\n✓ Material updated successfully!")
        else:
            print(f"\n✗ Failed to update material.")
    
    def delete_material(self):
        """Delete a material"""
        self.print_header("Delete Material")
        
        materials = self.calculator.get_all_materials()
        self.print_materials_table(materials)
        
        if not materials:
            return
        
        try:
            material_id = int(input("\nEnter material ID to delete: ").strip())
        except ValueError:
            print("Error: Invalid ID format.")
            return
        
        material = self.calculator.get_material_by_id(material_id)
        if not material:
            print(f"Error: Material with ID {material_id} not found.")
            return
        
        confirm = input(f"Are you sure you want to delete '{material['name']}'? (yes/no): ").strip().lower()
        if confirm == 'yes':
            if self.calculator.delete_material(material_id):
                print(f"\n✓ Material deleted successfully!")
            else:
                print(f"\n✗ Failed to delete material.")
        else:
            print("Deletion cancelled.")
    
    def record_usage_menu(self):
        """Record usage of a material"""
        self.print_header("Record Material Usage")
        
        materials = self.calculator.get_all_materials()
        self.print_materials_table(materials)
        
        if not materials:
            print("\nNo materials available. Please add materials first.")
            input("\nPress Enter to continue...")
            return
        
        try:
            material_id = int(input("\nEnter material ID: ").strip())
        except ValueError:
            print("Error: Invalid ID format.")
            input("\nPress Enter to continue...")
            return
        
        material = self.calculator.get_material_by_id(material_id)
        if not material:
            print(f"Error: Material with ID {material_id} not found.")
            input("\nPress Enter to continue...")
            return
        
        try:
            quantity = float(input(f"Enter quantity ({material['unit']}): ").strip())
            if quantity <= 0:
                print("Error: Quantity must be positive.")
                input("\nPress Enter to continue...")
                return
        except ValueError:
            print("Error: Invalid quantity format.")
            input("\nPress Enter to continue...")
            return
        
        purpose = input("Enter purpose (optional): ").strip()
        
        if self.calculator.record_usage(material_id, quantity, purpose):
            cost = quantity * material['unit_price']
            print(f"\n✓ Usage recorded successfully!")
            print(f"   Material: {material['name']}")
            print(f"   Quantity: {quantity} {material['unit']}")
            print(f"   Cost: ${cost:.2f}")
        else:
            print(f"\n✗ Failed to record usage.")
        
        input("\nPress Enter to continue...")
    
    def view_inventory_menu(self):
        """View inventory with usage summary"""
        self.print_header("Inventory Summary")
        
        summary = self.calculator.get_material_summary()
        
        if not summary:
            print("\nNo materials in inventory.")
            input("\nPress Enter to continue...")
            return
        
        print("\n{:<5} {:<20} {:<10} {:<12} {:<15} {:<15}".format(
            "ID", "Name", "Unit", "Unit Price", "Total Usage", "Total Cost"
        ))
        print("-" * 85)
        
        grand_total = 0.0
        for row in summary:
            print("{:<5} {:<20} {:<10} ${:<11.2f} {:<15.2f} ${:<14.2f}".format(
                row['id'], row['name'][:20], row['unit'], row['unit_price'],
                row['total_quantity'], row['total_cost']
            ))
            grand_total += row['total_cost']
        
        print("-" * 85)
        print(f"{'Grand Total:':<70} ${grand_total:.2f}")
        
        input("\nPress Enter to continue...")
    
    def view_usage_history_menu(self):
        """View and filter usage history"""
        while True:
            self.print_header("Usage History")
            print("\n1. View All Usage")
            print("2. Filter by Material")
            print("3. Filter by Purpose")
            print("4. Back to Main Menu")
            print()
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                self.view_all_usage()
            elif choice == '2':
                self.filter_usage_by_material()
            elif choice == '3':
                self.filter_usage_by_purpose()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def view_all_usage(self):
        """View all usage records"""
        self.print_header("All Usage Records")
        
        usage_records = self.calculator.get_all_usage()
        self.print_usage_table(usage_records)
        
        if usage_records:
            total_cost = self.calculator.calculate_total_cost()
            print(f"\nTotal Cost: ${total_cost:.2f}")
        
        input("\nPress Enter to continue...")
    
    def filter_usage_by_material(self):
        """Filter usage records by material"""
        self.print_header("Filter Usage by Material")
        
        materials = self.calculator.get_all_materials()
        self.print_materials_table(materials)
        
        if not materials:
            return
        
        try:
            material_id = int(input("\nEnter material ID: ").strip())
        except ValueError:
            print("Error: Invalid ID format.")
            input("\nPress Enter to continue...")
            return
        
        material = self.calculator.get_material_by_id(material_id)
        if not material:
            print(f"Error: Material with ID {material_id} not found.")
            input("\nPress Enter to continue...")
            return
        
        usage_records = self.calculator.get_usage_by_material(material_id)
        self.print_usage_table(usage_records)
        
        if usage_records:
            total_cost = self.calculator.calculate_total_cost(material_id)
            print(f"\nTotal Cost for {material['name']}: ${total_cost:.2f}")
        
        input("\nPress Enter to continue...")
    
    def filter_usage_by_purpose(self):
        """Filter usage records by purpose"""
        self.print_header("Filter Usage by Purpose")
        
        purpose = input("\nEnter purpose to search for: ").strip()
        if not purpose:
            print("Error: Purpose cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        usage_records = self.calculator.get_usage_by_purpose(purpose)
        self.print_usage_table(usage_records)
        
        input("\nPress Enter to continue...")
    
    def calculate_costs_menu(self):
        """Display cost calculations"""
        while True:
            self.print_header("Cost Calculations")
            print("\n1. Total Cost (All Materials)")
            print("2. Cost by Material")
            print("3. Back to Main Menu")
            print()
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                self.show_total_cost()
            elif choice == '2':
                self.show_cost_by_material()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def show_total_cost(self):
        """Show total cost of all usage"""
        self.print_header("Total Cost - All Materials")
        
        total_cost = self.calculator.calculate_total_cost()
        print(f"\nTotal Cost of All Material Usage: ${total_cost:.2f}")
        
        input("\nPress Enter to continue...")
    
    def show_cost_by_material(self):
        """Show cost breakdown by material"""
        self.print_header("Cost by Material")
        
        materials = self.calculator.get_all_materials()
        self.print_materials_table(materials)
        
        if not materials:
            return
        
        try:
            material_id = int(input("\nEnter material ID: ").strip())
        except ValueError:
            print("Error: Invalid ID format.")
            input("\nPress Enter to continue...")
            return
        
        material = self.calculator.get_material_by_id(material_id)
        if not material:
            print(f"Error: Material with ID {material_id} not found.")
            input("\nPress Enter to continue...")
            return
        
        total_cost = self.calculator.calculate_total_cost(material_id)
        print(f"\nTotal Cost for {material['name']}: ${total_cost:.2f}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                self.display_main_menu()
                choice = input("Enter your choice (1-6): ").strip()
                
                if choice == '1':
                    self.material_management_menu()
                elif choice == '2':
                    self.record_usage_menu()
                elif choice == '3':
                    self.view_inventory_menu()
                elif choice == '4':
                    self.view_usage_history_menu()
                elif choice == '5':
                    self.calculate_costs_menu()
                elif choice == '6':
                    print("\nThank you for using Material Usage Calculator!")
                    break
                else:
                    print("Invalid choice. Please try again.")
        
        finally:
            self.calculator.close()


def main():
    """Entry point for the application"""
    ui = MaterialCalculatorUI()
    ui.run()


if __name__ == "__main__":
    main()
