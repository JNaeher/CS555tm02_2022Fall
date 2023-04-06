from project import *
import unittest

#patel_test1.ged has no male with different names and no siblings are married
#patel_test2.ged has a male with different name
#patel_test3.ged has male with different name and siblings are married
#patel_test4.ged has two pairs of siblings married
#patel_test5.ged has a higher up male with a different last name 
#patel_test6.ged has every male in the family with different last names
#patel_test7.ged has youngest members of family married to their siblings
#patel_test8.ged has an entire family where all sibings are married to each other

class testMaleLastName(unittest.TestCase):
    #user story 16
    def test_maleone(self):
        self.assertTrue(male_lastname('patel_test1.ged'),"Failed Test case 1!")
    def test_maletwo(self):
        self.assertFalse(male_lastname('patel_test2.ged'),"Failed Test case 2!")
    def test_malethree(self):
        self.assertFalse(male_lastname('patel_test3.ged'),"Failed Test case 3!")
    def test_malefour(self):
        self.assertFalse(male_lastname('patel_test5.ged'),"Failed Test case 5!")
    def test_malefive(self):
        self.assertFalse(male_lastname('patel_test6.ged'),"Failed Test case 6!")
class testSibsNoMarry(unittest.TestCase):
    #user story 18
    def test_sibsone(self):
        self.assertTrue(sibs_nomarry('patel_test3.ged'),"Failed Test case 3!")
    def test_sibstwo(self):
        self.assertTrue(sibs_nomarry('patel_test1.ged'),"Failed Test case 1!")
    def test_sibsthree(self):
        self.assertTrue(sibs_nomarry('patel_test4.ged'),"Failed Test case 4!")
    def test_sibsfour(self):
        self.assertTrue(sibs_nomarry('patel_test7.ged'),"Failed Test case 7!")
    def test_sibsfive(self):
        self.assertTrue(sibs_nomarry('patel_test8.ged'),"Failed Test case 8!")