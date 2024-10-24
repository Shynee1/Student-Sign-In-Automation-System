import unittest
from school_schedule import registration_open, free_period
from datetime import datetime

class TestSchoolSchedule(unittest.TestCase):
    def test_free_period_first_day(self):
        self.assertEqual(free_period(datetime(2022, 9, 8)), "A")
    
    def test_free_period_known_day(self):
        self.assertEqual(free_period(datetime(2023, 3, 20)), "E")
        
    def test_registration_open_early(self):
        self.assertFalse(registration_open(datetime(2023, 3, 14, 6, 0)))
        
    def test_registration_open_late(self):
        self.assertFalse(registration_open(datetime(2023, 3, 14, 10, 0)))
        
    def test_registration_open_wednesday(self):
        self.assertTrue(registration_open(datetime(2023, 3, 15, 10, 0)))
        
    def test_registration_open_first_day(self):
        self.assertTrue(registration_open(datetime(2022, 9, 8, 7, 0)))
        
    def test_registration_open_ontime(self):
        self.assertTrue(registration_open(datetime(2023, 3, 14, 9, 37)))
        
    def test_registration_open_weekend(self):
        self.assertFalse(registration_open(datetime(2023, 3, 12, 9, 37)))
        
if __name__ == '__main__':
    unittest.main()
