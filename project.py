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
                person['age'] = get_age(person)
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
    ids = []
    dup_ids = []
    value = True
    for person in individuals:
        ids.append(person['ID'])
    
    for x in range(len(ids)):
        if(x == len(ids)-1):
            return value
        elif(exists(ids[x], ids[x+1:])):
            value = False
            if(exists(ids[x], dup_ids)):
                continue
            else:
                dup_ids.append(ids[x])
                print("Error US22: Individual ID " + "(" + ids[x] + ") is a duplicate.")

    return value

def unique_family_id(filename):
    data = organize(filename)
    families = data[1]
    ids = []
    dup_ids = []
    value = True

    for family in families:
        ids.append(family['ID'])
    
    for x in range(len(ids)):
        if(x == len(ids)-1):
            return value
        elif(exists(ids[x], ids[x+1:])):
            value = False
            if(exists(ids[x], dup_ids)):
                continue
            else:
                dup_ids.append(ids[x])
                print("Error US22: Family ID " + "(" + ids[x] + ") is a duplicate.")
                
    return value
    
# user story 42: reject illegitimate dates
def date_helper(day, month):
    day = int(day)
    if day < 1 or day > 31:
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

    value = True
    
    #check dates for individuals
    for person in individuals:

        birthday = person['birthday']
        deathday = person['death']

        if(birthday == None):
            birthday = "1 JAN 2000"
        if(deathday == None):
            deathday = "1 JAN 2000"

        birthday = birthday.split(" ", 2)
        deathday = deathday.split(" ", 2)

        if(len(birthday) == 2):
            if(exists(birthday[0], months) == False):
                value = False
                print("Error US42: " + person['name'] + " has an illegitimate birthday.")

        if(len(deathday) == 2):
            if(exists(deathday[0], months) == False):
                value = False
                print("Error US42: " + person['name'] + " has an illegitimate death date.")

        if(len(birthday) == 3):
            if(date_helper(birthday[0], birthday[1]) == False):
                value = False
                print("Error US42: " + person['name'] + " has an illegitimate birthday.")

        if(len(deathday) == 3):
            if(date_helper(deathday[0], deathday[1]) == False):
                value = False
                print("Error US42: " + person['name'] + " has an illegitimate death date.")

    #check dates for families

    for family in families:
        marriage = family['married']
        divorce = family['divorced']

        if(marriage == None):
            marriage = "1 JAN 2000"
        if(divorce == None):
            divorce = "1 JAN 2000"

        marriage = marriage.split(" ", 2)
        divorce = divorce.split(" ", 2)

        if(len(marriage) == 2):
            if(exists(marriage[0], months) == False):
                value = False
                print("Error US42: " + family['ID'] + " has an illegitimate marriage date.")

        if(len(divorce) == 2):
            if(exists(divorce[0], months) == False):
                value = False
                print("Error US42: " + family['ID'] + " has an illegitimate divorce date.")

        if(len(marriage) == 3):
            if(date_helper(marriage[0], marriage[1]) == False):
                value = False
                print("Error US42: " + family['ID'] + " has an illegitimate marriage date.")

        if(len(divorce) == 3):
            if(date_helper(divorce[0], divorce[1]) == False):
                value = False
                print("Error US42: " + family['ID'] + " has an illegitimate divorce date.")

    return value

# convert date string to date type
def string_to_date(string):
    if string is None:
        return None
    temp = string.split(" ", 2)
    day = int(temp[0])
    year = int(temp[2])
    month = 0
    if(temp[1] == 'JAN'):
        month = 1
    if(temp[1] == 'FEB'):
        month = 2
    if(temp[1] == 'MAR'):
        month = 3
    if(temp[1] == 'APR'):
        month = 4
    if(temp[1] == 'MAY'):
        month = 5
    if(temp[1] == 'JUN'):
        month = 6
    if(temp[1] == 'JUL'):
        month = 7
    if(temp[1] == 'AUG'):
        month = 8
    if(temp[1] == 'SEP'):
        month = 9
    if(temp[1] == 'OCT'):
        month = 10
    if(temp[1] == 'NOV'):
        month = 11
    if(temp[1] == 'DEC'):
        month = 12
    return date(year, month, day)

# returns the diffence between 2 date strings
# in terms of months
def find_month_differance(start, end):
    dateStart = string_to_date(start)
    dateEnd = string_to_date(end)
    return (dateStart - dateEnd).days / 30.417

# user story 09: Birth Before Death of Parents
# check if birth's happen before death of the mother 
# and 9 months before the death of the father
def valid_birth(data):
    individuals = data[0]
    families = data[1]
    validBirthdays = True
    for fam in families:
        if(len(fam['children']) > 0):
            hid = fam['hid']
            wid = fam['wid']
            children = []
            for person in individuals:
                if person['ID'] == hid:
                    hus = person
                if person['ID'] == wid:
                    wif = person
                for child in fam['children']:
                    if person['ID'] == child:
                        children.append(person)
            if (wif['death'] != None or hus['death'] != None):
                for child in children:
                    if (wif['death'] != None):
                        if(find_month_differance(child['birthday'],wif['death']) > 0):
                            validBirthdays = False
                            print('Error US09: ' + wif['name'] + "'s Death is before " + child['name'] + "'s Birth")
                    if (hus['death'] != None):
                        if(find_month_differance(child['birthday'],hus['death']) > 9):
                            validBirthdays = False
                            print('Anomaly US09: ' + hus['name'] + "'s Death more than 9 months before " + child['name'] + "'s Birth")
    return(validBirthdays)

# user story 27 get persons age
def get_age(person):
    if(person['birthday'] == None):
        return -1
    elif(person['death'] == None):
        birthday = string_to_date(person['birthday'])
        age = int((date.today() - birthday).days / 365)
        return age
    else:
        birthday = string_to_date(person['birthday'])
        death = string_to_date(person['death'])
        age = int((death - birthday).days / 365)
        return age

def main():
    #getting data from the file given from command line
    fname = sys.argv[1]
    data = organize(fname)
    individuals = data[0]
    families = data[1]

    #prints the tables
    printIndividuals(individuals, families)
    printFamilies(individuals, families)

    #does the checking from the user stories

    #user story 09
    if(valid_birth(data) == True):
        print("Correct US09: All Children born while parents where alive")

    #user story 22
    if(unique_indiv_id(fname) == True):
        print("Correct US22: All individual IDs are unique.")
    
    if(unique_family_id(fname) == True):
        print("Correct US22: All family IDs are unique.")

    #user story 42
    if(date_checker(fname) == True):
        print("Correct US42: All dates are legitimate")


    return 

if __name__ == "__main__":
    main()