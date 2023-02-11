from project import *
import unittest

class TestUniqueID(unittest.TestCase):
    def test_individual1(self):
        self.assertEqual(unique_indiv_id('project1.ged'), True)

    def test_individual2(self):
        self.assertEqual(unique_indiv_id('test1.ged'), True)

    def test_family1(self):
        self.assertEqual(unique_family_id('project1.ged'), True)