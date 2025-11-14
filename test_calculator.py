#!/usr/bin/env python3
"""
Test script for Material Usage Calculator
Tests the core functionality of the application.
"""

import os
import sys
import sqlite3

# Import the calculator module
from material_calculator import MaterialUsageCalculator


def test_database_setup():
    """Test database creation and schema."""
    print("\n=== Testing Database Setup ===")
    
    # Use a test database
    test_db = 'test_material_usage.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    
    calc = MaterialUsageCalculator(test_db)
    
    # Check if tables exist
    calc.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in calc.cursor.fetchall()]
    
    assert 'materials' in tables, "Materials table not created"
    assert 'usage' in tables, "Usage table not created"
    print("✓ Database tables created successfully")
    
    calc.close()
    os.remove(test_db)
    return True


def test_add_material():
    """Test adding materials."""
    print("\n=== Testing Add Material ===")
    
    test_db = 'test_material_usage.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    
    calc = MaterialUsageCalculator(test_db)
    
    # Add a material
    result = calc.add_material("Cement", "kg", 5.50)
    assert result == True, "Failed to add material"
    print("✓ Material added successfully")
    
    # Try to add duplicate (should fail)
    result = calc.add_material("Cement", "kg", 5.50)
    assert result == False, "Duplicate material should not be added"
    print("✓ Duplicate prevention works")
    
    # Verify material in database
    calc.cursor.execute("SELECT name, unit, unit_price FROM materials WHERE name='Cement'")
    row = calc.cursor.fetchone()
    assert row[0] == "Cement", "Material name not saved correctly"
    assert row[1] == "kg", "Material unit not saved correctly"
    assert row[2] == 5.50, "Material price not saved correctly"
    print("✓ Material data stored correctly")
    
    calc.close()
    os.remove(test_db)
    return True


def test_record_usage():
    """Test recording material usage."""
    print("\n=== Testing Record Usage ===")
    
    test_db = 'test_material_usage.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    
    calc = MaterialUsageCalculator(test_db)
    
    # Add a material first
    calc.add_material("Steel", "kg", 10.00)
    
    # Record usage
    result = calc.record_usage("Steel", 25.5, "Building foundation")
    assert result == True, "Failed to record usage"
    print("✓ Usage recorded successfully")
    
    # Try to record usage for non-existent material
    result = calc.record_usage("NonExistent", 10.0)
    assert result == False, "Should fail for non-existent material"
    print("✓ Non-existent material handling works")
    
    # Verify usage in database
    calc.cursor.execute("""
        SELECT u.quantity, u.purpose, m.name 
        FROM usage u 
        JOIN materials m ON u.material_id = m.id 
        WHERE m.name='Steel'
    """)
    row = calc.cursor.fetchone()
    assert row[0] == 25.5, "Usage quantity not saved correctly"
    assert row[1] == "Building foundation", "Usage purpose not saved correctly"
    assert row[2] == "Steel", "Material relationship not correct"
    print("✓ Usage data stored correctly")
    
    calc.close()
    os.remove(test_db)
    return True


def test_view_materials():
    """Test viewing materials."""
    print("\n=== Testing View Materials ===")
    
    test_db = 'test_material_usage.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    
    calc = MaterialUsageCalculator(test_db)
    
    # Add multiple materials
    calc.add_material("Cement", "kg", 5.50)
    calc.add_material("Steel", "kg", 10.00)
    calc.add_material("Sand", "tons", 20.00)
    
    # This should print the materials
    print("\nMaterial list output:")
    calc.view_materials()
    
    # Verify count
    calc.cursor.execute("SELECT COUNT(*) FROM materials")
    count = calc.cursor.fetchone()[0]
    assert count == 3, f"Expected 3 materials, found {count}"
    print(f"✓ All {count} materials can be viewed")
    
    calc.close()
    os.remove(test_db)
    return True


def test_calculate_total():
    """Test calculating total usage and cost."""
    print("\n=== Testing Calculate Total ===")
    
    test_db = 'test_material_usage.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    
    calc = MaterialUsageCalculator(test_db)
    
    # Add materials
    calc.add_material("Cement", "kg", 5.00)
    calc.add_material("Steel", "kg", 10.00)
    
    # Record usage
    calc.record_usage("Cement", 100.0, "Foundation")
    calc.record_usage("Cement", 50.0, "Walls")
    calc.record_usage("Steel", 25.0, "Beams")
    
    # Calculate totals (this will print the results)
    print("\nTotal usage output:")
    calc.calculate_total_usage()
    
    # Verify calculations manually
    calc.cursor.execute("""
        SELECT m.name, SUM(u.quantity), SUM(u.quantity * m.unit_price)
        FROM materials m
        LEFT JOIN usage u ON m.id = u.material_id
        WHERE m.name = 'Cement'
        GROUP BY m.name
    """)
    row = calc.cursor.fetchone()
    assert row[1] == 150.0, "Cement total quantity incorrect"
    assert row[2] == 750.0, "Cement total cost incorrect"
    print("✓ Calculations are correct")
    
    calc.close()
    os.remove(test_db)
    return True


def main():
    """Run all tests."""
    print("╔════════════════════════════════════════════════╗")
    print("║   Material Usage Calculator - Test Suite      ║")
    print("╚════════════════════════════════════════════════╝")
    
    tests = [
        test_database_setup,
        test_add_material,
        test_record_usage,
        test_view_materials,
        test_calculate_total,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print(f"✓ {test.__name__} PASSED")
        except AssertionError as e:
            failed += 1
            print(f"✗ {test.__name__} FAILED: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} ERROR: {e}")
    
    print("\n" + "="*50)
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print("="*50)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
