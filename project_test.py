from project import *
import unittest

class TestUniqueID(unittest.TestCase):
    def test_individual(self):
        self.assertEqual(unique_indiv_id('project1.ged'), True)