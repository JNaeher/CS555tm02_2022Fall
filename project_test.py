from project import *
import unittest

class TestUniqueID(unittest.TestCase):
    # naeher_test1 has unique ids for both individuals and families
    # naeher_test2 has unique ids for both individuals and families
    # naeher_test3 has duplicate ids for both inidividuals and families
    def test_individual1(self):
        self.assertEqual(unique_indiv_id('naeher_test1.ged'), True)

    def test_individual2(self):
        self.assertEqual(unique_indiv_id('naeher_test2.ged'), True)
    
    def test_individual3(self):
        self.assertEqual(unique_indiv_id('naeher_test3.ged'), False)

    def test_family1(self):
        self.assertEqual(unique_family_id('naeher_test1.ged'), True)

    def test_family2(self):
        self.assertEqual(unique_family_id('naeher_test3.ged'), False)