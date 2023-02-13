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

class TestIllegitimateDates(unittest.TestCase):
    # naeher_test1 has legitimate dates
    # naeher_test3 has an illegitimate death date
    # naeher_test4 has an illegitimate birth date
    # naeher_test5 has an illegitimate marriage date
    # naeher_test6 has an illegitimate divorce date
    def test_date1(self):
        self.assertEqual(date_checker('naeher_test1.ged'), True)

    def test_date2(self):
        self.assertEqual(date_checker('naeher_test3.ged'), False)

    def test_date3(self):
        self.assertEqual(date_checker('naeher_test4.ged'), False)

    def test_date4(self):
        self.assertEqual(date_checker('naeher_test5.ged'), False)

    def test_date5(self):
        self.assertEqual(date_checker('naeher_test6.ged'), False)
