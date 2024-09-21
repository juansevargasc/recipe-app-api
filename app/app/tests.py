"""
Sample Tests
"""
from django.test import SimpleTestCase
from app import calc

class CalcTests(SimpleTestCase):
    """Test the calc module."""
    
    def test_add_numbers(self):
        """Test adding numbers."""
        res = calc.add(5, 6)
        
        self.assertEqual(res, 11)
    
    def test_substract(self):
        """Test substracting two numbers."""
        res = calc.substract(10, 5)
        
        self.assertEqual(res, 5)