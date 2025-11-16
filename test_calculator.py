#!/usr/bin/env python3
"""
Unit tests for Material Usage Calculator
"""
import unittest
import sqlite3
import os
import tempfile
from datetime import datetime
from material_calculator import MaterialCalculator


class TestMaterialCalculator(unittest.TestCase):
    """Test cases for MaterialCalculator class"""
    
    def setUp(self):
        """Set up test database before each test"""
        # Create a temporary database file
        self.test_db_fd, self.test_db_path = tempfile.mkstemp(suffix='.db')
        self.calculator = MaterialCalculator(self.test_db_path)
    
    def tearDown(self):
        """Clean up test database after each test"""
        self.calculator.close()
        os.close(self.test_db_fd)
        os.unlink(self.test_db_path)
    
    def test_database_setup(self):
        """Test that database tables are created correctly"""
        cursor = self.calculator.conn.cursor()
        
        # Check materials table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='materials'
        """)
        self.assertIsNotNone(cursor.fetchone())
        
        # Check usage table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='usage'
        """)
        self.assertIsNotNone(cursor.fetchone())
        
        # Check materials table schema
        cursor.execute("PRAGMA table_info(materials)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        self.assertIn('name', columns)
        self.assertIn('unit', columns)
        self.assertIn('unit_price', columns)
        
        # Check usage table schema
        cursor.execute("PRAGMA table_info(usage)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        self.assertIn('material_id', columns)
        self.assertIn('quantity', columns)
        self.assertIn('purpose', columns)
        self.assertIn('timestamp', columns)
    
    def test_add_material(self):
        """Test adding a new material"""
        result = self.calculator.add_material("Steel", "kg", 5.50)
        self.assertTrue(result)
        
        # Verify material was added
        materials = self.calculator.get_all_materials()
        self.assertEqual(len(materials), 1)
        self.assertEqual(materials[0]['name'], "Steel")
        self.assertEqual(materials[0]['unit'], "kg")
        self.assertEqual(materials[0]['unit_price'], 5.50)
    
    def test_add_duplicate_material(self):
        """Test that adding duplicate material fails"""
        self.calculator.add_material("Steel", "kg", 5.50)
        result = self.calculator.add_material("Steel", "tons", 10.00)
        self.assertFalse(result)
        
        # Verify only one material exists
        materials = self.calculator.get_all_materials()
        self.assertEqual(len(materials), 1)
    
    def test_get_all_materials(self):
        """Test retrieving all materials"""
        self.calculator.add_material("Steel", "kg", 5.50)
        self.calculator.add_material("Cement", "bags", 12.00)
        self.calculator.add_material("Wood", "planks", 8.75)
        
        materials = self.calculator.get_all_materials()
        self.assertEqual(len(materials), 3)
        
        # Check they're sorted by name
        names = [m['name'] for m in materials]
        self.assertEqual(names, ["Cement", "Steel", "Wood"])
    
    def test_get_material_by_id(self):
        """Test retrieving a material by ID"""
        self.calculator.add_material("Steel", "kg", 5.50)
        materials = self.calculator.get_all_materials()
        material_id = materials[0]['id']
        
        material = self.calculator.get_material_by_id(material_id)
        self.assertIsNotNone(material)
        self.assertEqual(material['name'], "Steel")
        
        # Test non-existent ID
        material = self.calculator.get_material_by_id(9999)
        self.assertIsNone(material)
    
    def test_get_material_by_name(self):
        """Test retrieving a material by name"""
        self.calculator.add_material("Steel", "kg", 5.50)
        
        material = self.calculator.get_material_by_name("Steel")
        self.assertIsNotNone(material)
        self.assertEqual(material['unit'], "kg")
        self.assertEqual(material['unit_price'], 5.50)
        
        # Test non-existent name
        material = self.calculator.get_material_by_name("NonExistent")
        self.assertIsNone(material)
    
    def test_update_material(self):
        """Test updating a material"""
        self.calculator.add_material("Steel", "kg", 5.50)
        materials = self.calculator.get_all_materials()
        material_id = materials[0]['id']
        
        result = self.calculator.update_material(material_id, "Steel Grade A", "tons", 6.00)
        self.assertTrue(result)
        
        # Verify update
        material = self.calculator.get_material_by_id(material_id)
        self.assertEqual(material['name'], "Steel Grade A")
        self.assertEqual(material['unit'], "tons")
        self.assertEqual(material['unit_price'], 6.00)
    
    def test_update_nonexistent_material(self):
        """Test updating a non-existent material"""
        result = self.calculator.update_material(9999, "Test", "unit", 1.0)
        self.assertFalse(result)
    
    def test_delete_material(self):
        """Test deleting a material"""
        self.calculator.add_material("Steel", "kg", 5.50)
        materials = self.calculator.get_all_materials()
        material_id = materials[0]['id']
        
        result = self.calculator.delete_material(material_id)
        self.assertTrue(result)
        
        # Verify deletion
        materials = self.calculator.get_all_materials()
        self.assertEqual(len(materials), 0)
    
    def test_delete_nonexistent_material(self):
        """Test deleting a non-existent material"""
        result = self.calculator.delete_material(9999)
        self.assertFalse(result)
    
    def test_record_usage(self):
        """Test recording material usage"""
        self.calculator.add_material("Steel", "kg", 5.50)
        materials = self.calculator.get_all_materials()
        material_id = materials[0]['id']
        
        result = self.calculator.record_usage(material_id, 100.5, "Construction project")
        self.assertTrue(result)
        
        # Verify usage was recorded
        usage_records = self.calculator.get_all_usage()
        self.assertEqual(len(usage_records), 1)
        self.assertEqual(usage_records[0]['material_id'], material_id)
        self.assertEqual(usage_records[0]['quantity'], 100.5)
        self.assertEqual(usage_records[0]['purpose'], "Construction project")
    
    def test_record_usage_without_purpose(self):
        """Test recording usage without purpose"""
        self.calculator.add_material("Steel", "kg", 5.50)
        materials = self.calculator.get_all_materials()
        material_id = materials[0]['id']
        
        result = self.calculator.record_usage(material_id, 50.0)
        self.assertTrue(result)
        
        usage_records = self.calculator.get_all_usage()
        self.assertEqual(len(usage_records), 1)
        self.assertEqual(usage_records[0]['purpose'], "")
    
    def test_get_all_usage(self):
        """Test retrieving all usage records"""
        self.calculator.add_material("Steel", "kg", 5.50)
        self.calculator.add_material("Cement", "bags", 12.00)
        
        steel = self.calculator.get_material_by_name("Steel")
        cement = self.calculator.get_material_by_name("Cement")
        
        self.calculator.record_usage(steel['id'], 100, "Project A")
        self.calculator.record_usage(cement['id'], 50, "Project B")
        self.calculator.record_usage(steel['id'], 75, "Project C")
        
        usage_records = self.calculator.get_all_usage()
        self.assertEqual(len(usage_records), 3)
    
    def test_get_usage_by_material(self):
        """Test filtering usage by material"""
        self.calculator.add_material("Steel", "kg", 5.50)
        self.calculator.add_material("Cement", "bags", 12.00)
        
        steel = self.calculator.get_material_by_name("Steel")
        cement = self.calculator.get_material_by_name("Cement")
        
        self.calculator.record_usage(steel['id'], 100, "Project A")
        self.calculator.record_usage(cement['id'], 50, "Project B")
        self.calculator.record_usage(steel['id'], 75, "Project C")
        
        steel_usage = self.calculator.get_usage_by_material(steel['id'])
        self.assertEqual(len(steel_usage), 2)
        
        cement_usage = self.calculator.get_usage_by_material(cement['id'])
        self.assertEqual(len(cement_usage), 1)
    
    def test_get_usage_by_purpose(self):
        """Test filtering usage by purpose"""
        self.calculator.add_material("Steel", "kg", 5.50)
        
        material = self.calculator.get_material_by_name("Steel")
        
        self.calculator.record_usage(material['id'], 100, "Construction")
        self.calculator.record_usage(material['id'], 50, "Renovation")
        self.calculator.record_usage(material['id'], 75, "Construction Phase 2")
        
        construction_usage = self.calculator.get_usage_by_purpose("Construction")
        self.assertEqual(len(construction_usage), 2)
        
        renovation_usage = self.calculator.get_usage_by_purpose("Renovation")
        self.assertEqual(len(renovation_usage), 1)
    
    def test_calculate_total_cost(self):
        """Test calculating total cost of all usage"""
        self.calculator.add_material("Steel", "kg", 5.50)
        self.calculator.add_material("Cement", "bags", 12.00)
        
        steel = self.calculator.get_material_by_name("Steel")
        cement = self.calculator.get_material_by_name("Cement")
        
        self.calculator.record_usage(steel['id'], 100, "Project A")  # 100 * 5.50 = 550
        self.calculator.record_usage(cement['id'], 50, "Project B")  # 50 * 12.00 = 600
        self.calculator.record_usage(steel['id'], 75, "Project C")   # 75 * 5.50 = 412.5
        
        total_cost = self.calculator.calculate_total_cost()
        self.assertAlmostEqual(total_cost, 1562.5, places=2)
    
    def test_calculate_total_cost_by_material(self):
        """Test calculating total cost for a specific material"""
        self.calculator.add_material("Steel", "kg", 5.50)
        self.calculator.add_material("Cement", "bags", 12.00)
        
        steel = self.calculator.get_material_by_name("Steel")
        cement = self.calculator.get_material_by_name("Cement")
        
        self.calculator.record_usage(steel['id'], 100, "Project A")  # 100 * 5.50 = 550
        self.calculator.record_usage(cement['id'], 50, "Project B")  # 50 * 12.00 = 600
        self.calculator.record_usage(steel['id'], 75, "Project C")   # 75 * 5.50 = 412.5
        
        steel_cost = self.calculator.calculate_total_cost(steel['id'])
        self.assertAlmostEqual(steel_cost, 962.5, places=2)
        
        cement_cost = self.calculator.calculate_total_cost(cement['id'])
        self.assertAlmostEqual(cement_cost, 600.0, places=2)
    
    def test_calculate_total_cost_no_usage(self):
        """Test calculating cost when there's no usage"""
        self.calculator.add_material("Steel", "kg", 5.50)
        
        total_cost = self.calculator.calculate_total_cost()
        self.assertEqual(total_cost, 0.0)
    
    def test_get_material_summary(self):
        """Test getting material summary with usage aggregation"""
        self.calculator.add_material("Steel", "kg", 5.50)
        self.calculator.add_material("Cement", "bags", 12.00)
        self.calculator.add_material("Wood", "planks", 8.00)
        
        steel = self.calculator.get_material_by_name("Steel")
        cement = self.calculator.get_material_by_name("Cement")
        # Wood has no usage
        
        self.calculator.record_usage(steel['id'], 100, "Project A")
        self.calculator.record_usage(steel['id'], 75, "Project B")
        self.calculator.record_usage(cement['id'], 50, "Project C")
        
        summary = self.calculator.get_material_summary()
        self.assertEqual(len(summary), 3)
        
        # Find steel in summary
        steel_summary = next(s for s in summary if s['name'] == 'Steel')
        self.assertAlmostEqual(steel_summary['total_quantity'], 175.0, places=2)
        self.assertAlmostEqual(steel_summary['total_cost'], 962.5, places=2)
        
        # Find cement in summary
        cement_summary = next(s for s in summary if s['name'] == 'Cement')
        self.assertAlmostEqual(cement_summary['total_quantity'], 50.0, places=2)
        self.assertAlmostEqual(cement_summary['total_cost'], 600.0, places=2)
        
        # Find wood in summary (no usage)
        wood_summary = next(s for s in summary if s['name'] == 'Wood')
        self.assertEqual(wood_summary['total_quantity'], 0.0)
        self.assertEqual(wood_summary['total_cost'], 0.0)
    
    def test_delete_material_with_usage(self):
        """Test that deleting a material also deletes its usage records"""
        self.calculator.add_material("Steel", "kg", 5.50)
        material = self.calculator.get_material_by_name("Steel")
        
        self.calculator.record_usage(material['id'], 100, "Project A")
        self.calculator.record_usage(material['id'], 75, "Project B")
        
        # Verify usage exists
        usage_records = self.calculator.get_all_usage()
        self.assertEqual(len(usage_records), 2)
        
        # Delete material
        self.calculator.delete_material(material['id'])
        
        # Verify usage is also deleted
        usage_records = self.calculator.get_all_usage()
        self.assertEqual(len(usage_records), 0)
    
    def test_usage_timestamp_format(self):
        """Test that usage records have valid ISO format timestamps"""
        self.calculator.add_material("Steel", "kg", 5.50)
        material = self.calculator.get_material_by_name("Steel")
        
        self.calculator.record_usage(material['id'], 100, "Project A")
        
        usage_records = self.calculator.get_all_usage()
        timestamp = usage_records[0]['timestamp']
        
        # Verify timestamp can be parsed as ISO format
        try:
            dt = datetime.fromisoformat(timestamp)
            self.assertIsInstance(dt, datetime)
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")
    
    def test_decimal_quantities(self):
        """Test handling of decimal quantities"""
        self.calculator.add_material("Steel", "kg", 5.50)
        material = self.calculator.get_material_by_name("Steel")
        
        self.calculator.record_usage(material['id'], 100.75, "Project A")
        self.calculator.record_usage(material['id'], 50.25, "Project B")
        
        total_cost = self.calculator.calculate_total_cost(material['id'])
        expected_cost = (100.75 + 50.25) * 5.50
        self.assertAlmostEqual(total_cost, expected_cost, places=2)
    
    def test_decimal_prices(self):
        """Test handling of decimal unit prices"""
        self.calculator.add_material("Steel", "kg", 5.55)
        material = self.calculator.get_material_by_name("Steel")
        
        self.calculator.record_usage(material['id'], 100, "Project A")
        
        total_cost = self.calculator.calculate_total_cost(material['id'])
        self.assertAlmostEqual(total_cost, 555.0, places=2)


class TestMaterialCalculatorEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""
    
    def setUp(self):
        """Set up test database before each test"""
        self.test_db_fd, self.test_db_path = tempfile.mkstemp(suffix='.db')
        self.calculator = MaterialCalculator(self.test_db_path)
    
    def tearDown(self):
        """Clean up test database after each test"""
        self.calculator.close()
        os.close(self.test_db_fd)
        os.unlink(self.test_db_path)
    
    def test_empty_database(self):
        """Test operations on empty database"""
        materials = self.calculator.get_all_materials()
        self.assertEqual(len(materials), 0)
        
        usage = self.calculator.get_all_usage()
        self.assertEqual(len(usage), 0)
        
        total_cost = self.calculator.calculate_total_cost()
        self.assertEqual(total_cost, 0.0)
    
    def test_special_characters_in_names(self):
        """Test materials with special characters in names"""
        self.calculator.add_material("Steel (Grade-A)", "kg", 5.50)
        self.calculator.add_material("Cement #1", "bags", 12.00)
        
        materials = self.calculator.get_all_materials()
        self.assertEqual(len(materials), 2)
    
    def test_unicode_characters(self):
        """Test materials with unicode characters"""
        self.calculator.add_material("Acero (Spanish)", "kg", 5.50)
        material = self.calculator.get_material_by_name("Acero (Spanish)")
        self.assertIsNotNone(material)
    
    def test_very_large_quantities(self):
        """Test handling of very large quantities"""
        self.calculator.add_material("Steel", "kg", 5.50)
        material = self.calculator.get_material_by_name("Steel")
        
        self.calculator.record_usage(material['id'], 1000000.0, "Large Project")
        
        total_cost = self.calculator.calculate_total_cost(material['id'])
        self.assertAlmostEqual(total_cost, 5500000.0, places=2)
    
    def test_zero_price(self):
        """Test material with zero price"""
        self.calculator.add_material("Free Material", "kg", 0.0)
        material = self.calculator.get_material_by_name("Free Material")
        
        self.calculator.record_usage(material['id'], 100, "Project")
        
        total_cost = self.calculator.calculate_total_cost(material['id'])
        self.assertEqual(total_cost, 0.0)


if __name__ == '__main__':
    unittest.main()
