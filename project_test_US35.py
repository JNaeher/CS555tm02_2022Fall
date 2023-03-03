from project import *
import unittest

class TestRecentBirth1(unittest.TestCase):
    # US09_test1_file.ged No births in the last 30 days
    # Expected to not return anyone
    def test_recent_birth1(self):
        print("\nTest 1:")
        data = organize('US09_test1_file.ged')
        self.assertEqual(recent_births_and_deaths(data)[0], [])

class TestRecentBirth2(unittest.TestCase):
    # US09_test2_file.ged Individual birth is in the last 30 days
    # Expected to return and individual Stormi Webster
    def test_recent_birth1(self):
        print("\nTest 2:")
        data = organize('US09_test2_file.ged')
        self.assertEqual(recent_births_and_deaths(data)[0], [{'ID': '@I24@','age': 0,'alive': True,'birthday': '27 FEB 2023','child': '@F7@','death': None,'gender': 'F','name': 'Stormi /Webster/','spouse': None}])

class TestRecentBirth3(unittest.TestCase):
    # US09_test3_file.ged Invalid Birth day in this case Stormi's birth of 30 FEB 2023 should return empty
    # Expected to not return anyone
    def test_recent_birth1(self):
        print("\nTest 3:")
        data = organize('US09_test3_file.ged')
        self.assertEqual(recent_births_and_deaths(data)[0], [])

class TestRecentBirth4(unittest.TestCase):
    # US09_test4_file.ged Mutiple Individual birth is in the last 30 days
    # Expected to return and individual Stormi Webster and Jake Neather
    def test_recent_birth1(self):
        print("\nTest 4:")
        data = organize('US09_test4_file.ged')
        self.assertEqual(recent_births_and_deaths(data)[0], [{'ID': '@I24@','age': 0,'alive': True,'birthday': '27 FEB 2023','child': '@F7@','death': None,'gender': 'F','name': 'Stormi /Webster/','spouse': None},
                                               {'ID': '@I25@','age': 0,'alive': True,'birthday': '1 MAR 2023','child': '@F2@','death': None,'gender': 'M','name': 'Jake /Naeher/','spouse': '@F9@'}])

