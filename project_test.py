from project import *
import unittest

class TestUS22(unittest.TestCase):
    def test_individual(self):
        self.assertEqual(unique_indiv_id('test_file.ged'), True)

class TestUS42(unittest.TestCase):
    def test_date(self):
        self.assertEqual(date_checker('test_file.ged'), True)

class TestUS29(unittest.TestCase):
    def test_dead(self):
        self.assertEqual(list_deceased('test_file.ged'), False)

class TestUS01(unittest.TestCase):
    def test_date(self):
        self.assertEqual(dates_after_current('test_file.ged'), True)

class TestUS16(unittest.TestCase):
    def test_malelastnames(self):
        self.assertEqual(male_lastname('test_file.ged'), False)

class TestUS18(unittest.TestCase):
    def test_sibs_nomarry(self):
        self.assertEqual(sibs_nomarry('test_file.ged'), True)

class TestUS12(unittest.TestCase):
    def test_parents_notold(self):
        self.assertEqual(parents_notold('test_file.ged'), True)

class TestUS30(unittest.TestCase):
    def test_livingmarried(self):
        self.assertEqual(livingmarried('test_file.ged'), True)

class TestUS35(unittest.TestCase):
    def test_recent_births(self):
        data = organize('test_file.ged')
        self.assertEqual(recent_births_and_deaths(data)[0], [{'ID': '@I24@','age': 0,'alive': True,'birthday': '27 FEB 2023','child': '@F7@','death': None,'gender': 'F','name': 'Stormi /Webster/','spouse': None}])

class TestUS36(unittest.TestCase):
    def test_recent_deaths(self):
        data = organize('test_file.ged')
        self.assertEqual(recent_births_and_deaths(data)[1], [{'ID': '@I5@','age': 8,'alive': False,'birthday': '14 DEC 2014','child': '@F1@','death': '27 FEB 2023','gender': 'F','name': 'Reign /Disick/','spouse': None}])

class TestUS23(unittest.TestCase):
    def test_unique_name_id(self):
        self.assertEqual(unique_name_id('test_file.ged'), True)

class TestUS25(unittest.TestCase):
    def test_unique_firstame_in_fam(self):
        self.assertEqual(unique_firstnames_in_fam('test_file.ged'), True)

class TestUS07(unittest.TestCase):
    def test_less_than_150(self):
        self.assertEqual(less_than_150('US07_failtest_file.ged'), False)

class TestUS17(unittest.TestCase):
    def test_no_marry_desc(self):
        self.assertEqual(no_marry_desc('US17_failtest_file.ged'), False) 

class TestUS14(unittest.TestCase):
    def test_multiple_births(self):
        self.assertEqual(multiple_births('test_file.ged'), True)

class TestUS19(unittest.TestCase):
    def test_first_cousins_nomarry(self):
        self.assertEqual(first_cousins_nomarry('test_file.ged'), True) 