from prettytable import PrettyTable
from datetime import date

#reminder: output into a file

tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

# checks to see if an element is in a list
def exists(elem, list):
    for a in list:
        if(a == elem):
            return True
    return False

# turns a string into a date object
def date_format(string):
    temp = string.split(" ", 2)
    if(len(temp) == 2):
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
        year = int(temp[1])
        return date(year, month)
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

# returns the age for someone who is alive
def age_alive(birth):
    return int((date.today() - birth).days / 365)

# returns the age for someone who is dead
def age_dead(birth, death):
    return int((death - birth).days / 365)

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
            person['death'] = 'N/A'
            person['age'] = age_alive(date_format(person['birthday']))
        else:
            person['alive'] = False
            person['age'] = age_dead(date_format(person['birthday']), date_format(person['death']))
    
    # gets the name of husband and wife for each family
    for family in fams:
        husb_id = family['hid']
        wife_id = family['wid']
        for person in indivs:
            if(husb_id == person['ID']):
                family['hname'] = person['name']
            if(wife_id == person['ID']):
                family['wname'] = person['name']
    
    # printIndividuals(indivs, fams)
    # printFamilies(indivs, fams)

    file.close()
    return [indivs, fams]

#user story 22: unique id's

#checking for unique individual ids
def unique_indiv_id(filename):
    data = organize(filename)
    individuals = data[0]
    ids = []
    for person in individuals:
        ids.append(person['ID'])
    
    for x in range(len(ids)):
        if(x == len(ids)-1):
            return True
        elif(exists(ids[x], ids[x+1:])):
            return False
    
    return True

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
    
