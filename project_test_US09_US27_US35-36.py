from project import *
import unittest

class TestValidBirth1(unittest.TestCase):
    # US09_test1_file.ged valid ged file normal births
    # Expected to succeed
    def test_valid_birth1(self):
        print("\nTest 1:")
        data = organize('US09_test1_file.ged')
        self.assertEqual(valid_birth(data), True)

class TestValidBirth2(unittest.TestCase):
    # US09_test2_file.ged Mother Death Before Birth
    # Expected to fail
    def test_valid_birth2(self):
        print("\nTest 2:")
        data = organize('US09_test2_file.ged')
        self.assertEqual(valid_birth(data), False)

class TestValidBirth3(unittest.TestCase):
    # US09_test3_file.ged Mother Death Day of Birth
    # Expected to succeed
    def test_valid_birth3(self):
        print("\nTest 3:")
        data = organize('US09_test3_file.ged')
        self.assertEqual(valid_birth(data), True)

class TestValidBirth4(unittest.TestCase):
    # US09_test4_file.ged Father Death is more than 9 months before child birth
    # Expected to fail
    def test_valid_birth4(self):
        print("\nTest 4:")
        data = organize('US09_test4_file.ged')
        self.assertEqual(valid_birth(data), False)

class TestValidBirth5(unittest.TestCase):
    # US09_test5_file.ged Father Death less than 9 months before child birth
    # Expected to succeed
    def test_valid_birth5(self):
        print("\nTest 5:")
        data = organize('US09_test5_file.ged')
        self.assertEqual(valid_birth(data), True)
