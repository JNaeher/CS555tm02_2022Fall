from prettytable import PrettyTable
from datetime import date
import sys

#reminder: output into a file

tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

# checks to see if an element is in a list
def exists(elem, list):
    for a in list:
        if(a == elem):
            return True
    return False

#checks if each tag is valid or not
# for line in array:
#     print("--> " + line)
#     temp = line.split(" ", 2)
#     if(exists(temp[1], tags) and len(temp) == 3):
#         print("<-- " + temp[0] + "|" + temp[1] + "|Y|" + temp[2])
#     elif(not exists(temp[1], tags) and len(temp) == 3):
#         print("<-- " + temp[0] + "|" + temp[1] + "|N|" + temp[2])
#     elif(exists(temp[1], tags) and len(temp) == 2):
#         print("<-- " + temp[0] + "|" + temp[1] + "|Y|")
#     elif(not exists(temp[1], tags) and len(temp) == 2):
#         print("<-- " + temp[0] + "|" + temp[1] + "|N|")
#     else:
#         if(temp[2] == 'INDI' or temp[2] == 'FAM'):
#             print("<-- " + temp[0] + "|" + temp[1] + "|Y|" + temp[2])
#         else:
#             print("<-- " + temp[0] + "|" + temp[1] + "|N|" + temp[2])

# helper function for storing information about individuals
def individual_helper(array, dictionary, indivs):
    for x in range(len(array)):
        temp = array[x].split(" ", 2)
        if(not (x == 0)):
            if(temp[0] == '0'):
                indivs.append(dictionary)
                return
        if(len(temp) == 3):
            if(temp[1] == 'NAME'):
                dictionary["name"] = temp[2]
            if(temp[1] == 'SEX'):
                dictionary["gender"] = temp[2]
            if(temp[1] == 'FAMS'):
                dictionary["spouse"] = temp[2]
            if(temp[1] == 'FAMC'):
                dictionary["child"] = temp[2]
            if(temp[1] == 'DEAT'):
                temp2 = array[x+1].split(" ", 2)
                dictionary["death"] = temp2[2]
        if(len(temp) == 2):
            if(temp[1] == 'BIRT'):
                temp2 = array[x+1].split(" ", 2)
                dictionary["birthday"] = temp2[2]
    indivs.append(dictionary)

# helper function for adding information about families
def family_helper(array, family, fams):
    for x in range(len(array)):
        temp = array[x].split(" ", 2)
        if(not (x == 0)):
            if(temp[0] == '0'):
                fams.append(family)
                return
        if(len(temp) == 3):
            if(temp[1] == 'HUSB'):
                family['hid'] = temp[2]
            if(temp[1] == 'WIFE'):
                family['wid'] = temp[2]
            if(temp[1] == 'CHIL'):
                family['children'].append(temp[2])
        if(len(temp) == 2):
            if(temp[1] == 'MARR'):
                temp2 = array[x+1].split(" ", 2)
                family['married'] =temp2[2]
            if(temp[1] == 'DIV'):
                temp2 = array[x+1].split(" ", 2)
                family['divorced'] = temp2[2]
    fams.append(family)
    return 0

def printIndividuals(indivs, fams):
    indivTable = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
    for person in indivs:
        temp = []
        temp.append(person['ID'])
        temp.append(person['name'])
        temp.append(person['gender'])
        temp.append(person['birthday'])
        temp.append(person['age'])
        temp.append(person['alive'])
        temp.append(person['death'])
        temp.append(person['child'])
        temp.append(person['spouse'])
        indivTable.add_row(temp)
    #prints the tables
    print("Individuals:")
    print(indivTable)

def printFamilies(indivs, fams):
    famTable = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])

    # adds each family to the table 
    for family in fams:
        temp = []
        temp.append(family['ID'])
        temp.append(family['married'])
        temp.append(family['divorced'])
        temp.append(family['hid'])
        temp.append(family['hname'])
        temp.append(family['wid'])
        temp.append(family['wname'])
        temp.append(family['children'])
        famTable.add_row(temp)

    # prints the table
    print("Families:")
    print(famTable)


def organize(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    array = []
    # gets rid of the end lines in the strings read from the file
    for line in lines:
        array.append(line.strip())

    # each individual will be saved as a dictionary with None values initially:
    # individual = {
    #     ID = None,
    #     name = None,
    #     gender = None,
    #     birthday = None,
    #     age = None,
    #     alive = None,
    #     death = None,
    #     child = None,
    #     spouse = None
    # }
    indivs = []

    # each family will be saved as a dictionary with None values initially
    # individual = {
    #     ID = None,
    #     married = None,
    #     divorced = None,
    #     hid = None,
    #     hname = None,
    #     wid = None,
    #     wname = None,
    #     children = None
    # }
    fams = []

    # main loop, goes through all the lines from the gedcom file
    # calls either individual helper or family helper depending on the line
    for x in range(len(array)):
        temp = array[x].split(" ", 2)
        if(len(temp) == 2 or len(temp) == 1):
            continue
        else:
            if(temp[2] == 'INDI'):
                person = dict(ID = temp[1], name = None, gender = None, birthday = None, age = None, alive = None, death = None, child = None, spouse = None)
                individual_helper(array[x+1:], person, indivs)
            if(temp[2] == 'FAM'):
                family = dict(ID = temp[1], married = None, divorced = None, hid = None, hname = None, wid = None, wname = None, children = [])
                family_helper(array[x+1:], family, fams)

    # to make the table look a bit better
    for person in indivs:
        if(person['death'] == None):
            person['alive'] = True
        else:
            person['alive'] = False
    
    # gets the name of husband and wife for each family
    for family in fams:
        husb_id = family['hid']
        wife_id = family['wid']
        for person in indivs:
            if(husb_id == person['ID']):
                family['hname'] = person['name']
            if(wife_id == person['ID']):
                family['wname'] = person['name']

    file.close()
    return [indivs, fams]

#user story 22: unique id's

#checking for unique individual ids
def unique_indiv_id(filename):
    data = organize(filename)
    individuals = data[0]
    ids_names = []
    ids = []
    value = True
    for person in individuals:
        ids_names.append([person['ID'], person['name']])
        ids.append(person['ID'])
    
    for x in range(len(ids)):
        if(x == len(ids)-1):
            return value
        elif(exists(ids[x], ids[x+1:])):
            value = False
            temp = ids_names[x]
            print("Error US22: ID " + "(" + temp[0] + ") is a duplicate.")

    
    return value

def unique_family_id(filename):
    data = organize(filename)
    families = data[1]
    ids = []
    for fam in families:
        ids.append(fam['ID'])

    for x in range(len(ids)):
        if(x == len(ids)-1):
            return True
        elif(exists(ids[x], ids[x+1:])):
            return False
    
    return True
    
# user story 42: reject illegitimate dates
def date_helper(day, month):
    day = int(day)
    if day < 1:
        return False
    if month == 'JAN' and day > 31:
        return False
    if month == 'FEB' and day > 28:
        return False
    if month == 'MAR' and day > 31:
        return False
    if month == 'APR' and day > 30:
        return False
    if month == 'MAY' and day > 31:
        return False
    if month == 'JUN' and day > 30:
        return False
    if month == 'JUL' and day > 31:
        return False
    if month == 'AUG' and day > 31:
        return False
    if month == 'SEP' and day > 30:
        return False
    if month == 'OCT' and day > 31:
        return False
    if month == 'NOV' and day > 30:
        return False
    if month == 'DEC' and day > 31:
        return False
    return True

def date_checker(filename):
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    birthdays = []
    deathdays = []
    marriages = []
    divorces = []

    for person in individuals:
        birthdays.append(person['birthday'])
        deathdays.append(person['death'])
    
    for family in families:
        marriages.append(family['married'])
        divorces.append(family['divorced'])

    # checking birthdates
    for x in range(len(birthdays)):
        if birthdays[x] is None:
            continue
        temp = birthdays[x].split(" ", 2)
        if(len(temp) == 2):
            if(exists(temp[0], months) == False):
                return False
        else:
            if(exists(temp[1], months) == False):
                return False
            else:
                if(date_helper(temp[0], temp[1]) == False):
                    return False

    #checking deathdates
    for x in range(len(deathdays)):
        if deathdays[x] is None:
            continue
        temp = deathdays[x].split(" ", 2)
        if(len(temp) == 2):
            if(exists(temp[0], months) == False):
                return False
        else:
            if(exists(temp[1], months) == False):
                return False
            else:
                if(date_helper(temp[0], temp[1]) == False):
                    return False
    
    #checking marriage dates
    for x in range(len(marriages)):
        if marriages[x] is None:
            continue
        temp = marriages[x].split(" ", 2)
        if(len(temp) == 2):
            if(exists(temp[0], months) == False):
                return False
        else:
            if(exists(temp[1], months) == False):
                return False
            else:
                if(date_helper(temp[0], temp[1]) == False):
                    return False

    #checking divorce dates
    for x in range(len(divorces)):
        if divorces[x] is None:
            continue
        temp = divorces[x].split(" ", 2)
        if(len(temp) == 2):
            if(exists(temp[0], months) == False):
                return False
        else:
            if(exists(temp[1], months) == False):
                return False
            else:
                if(date_helper(temp[0], temp[1]) == False):
                    return False

    #all dates check out
    return True

def main():
    fname = sys.argv[1]
    data = organize(fname)
    individuals = data[0]
    families = data[1]
    printIndividuals(individuals, families)
    printFamilies(individuals, families)
    unique_indiv_id(fname)
    return 

if __name__ == "__main__":
    main()