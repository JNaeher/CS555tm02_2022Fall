from project import *
import unittest

# USER STORY 06
class TestDivorcedBeforeDeath(unittest.TestCase): 
    # williamson_test1 has legitimate divorce dates
    # williamson_test2 has legitimate divorce dates
    # williamson_test3 has an illegitimate divorce date for both individuals
    # williamson_test4 has an illegitimate divorce date for one individual
    # williamson_test5 has two illegitimate divorce dates for two different marriages
    def test_date1(self):
        self.assertEqual(divorce_before_death('williamson_test1.ged'), True)

    def test_date2(self):
        self.assertEqual(divorce_before_death('williamson_test2.ged'), True)

    def test_date3(self):
        self.assertEqual(divorce_before_death('williamson_test3.ged'), False)

    def test_date4(self):
        self.assertEqual(divorce_before_death('williamson_test4.ged'), False)

    def test_date5(self):
        self.assertEqual(divorce_before_death('williamson_test5.ged'), False)

# USER STORY 10
class TestMarriedAfter14(unittest.TestCase):
    # williamson_test1 has legitimate marriage dates
    # williamson_test2 has legitimate marriage dates
    # williamson_test3 has an illegitimate marraige date for both individuals
    # williamson_test4 has an illegitimate marraige date for one individual
    # williamson_test5 has two illegitimate marriage dates for two different marriages
    def test_date1(self):
        self.assertEqual(marriage_after_14('williamson_test1.ged'), True)

    def test_date2(self):
        self.assertEqual(marriage_after_14('williamson_test2.ged'), True)

    def test_date3(self):
        self.assertEqual(marriage_after_14('williamson_test3.ged'), False)

    def test_date4(self):
        self.assertEqual(marriage_after_14('williamson_test4.ged'), False)

    def test_date5(self):
        self.assertEqual(marriage_after_14('williamson_test5.ged'), False)