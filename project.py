from unittest import skip
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
# user story 16: male last names
def male_lastname(filename):
    val=True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    for family in families:
        malename=family['hname']
        if(malename==None):
            break
        malename = malename.split(" ")
        headlastname = malename[1]
        children=family['children']
        for child in children:
            for check in individuals:
                if((child == check['ID']) and (check['gender']=='M')):
                    childname=check['name']
                    childname = childname.split(" ")
                    childlastname = childname[1]
                    if(childlastname!=headlastname):
                        print("Error US16: the males in the family " + family['ID'] + " do not all have the same last name.")
                        val=False
    return val

# user story 18: siblings cannot get married 
def sibs_nomarry(filename):
    spouse='NONE'
    val= True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    for fam in families:
        children= fam['children']
        for child in children:
            for check in individuals:
                if(child==check['ID']):
                    spouse=check['spouse']
            if (spouse in children):
                val= False
    return val 

#User Story 12: Parents not too old
def parents_notold(filename):
    val=True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    for fam in families:
        dad_id= fam['hid']
        mom_id= fam['wid']
        children= fam['children']
        #get ages of mother and father
        for dates in individuals:
            if(dad_id==dates['ID']):
                ddate=dates['birthday']
                ddate= ddate.split(" ")
                dday= ddate[0]
                dmonth= ddate[1]
                dyear= ddate[2]
            if(mom_id==dates['ID']):
                mdate=dates['birthday']
                mdate= mdate.split(" ")
                mday= mdate[0]
                mmonth= mdate[1]
                myear= mdate[2]
        for child in children:
            for check in individuals:
                if(child==check['ID']):
                    cdate=check['birthday']
                    cdate= cdate.split(" ")
                    cday= cdate[0]
                    cmonth= cdate[1]
                    cyear= cdate[2]
            if(int(dyear)-int(cyear)>80 or int(myear)-int(cyear)>60):
                val=False
    return val

#User Story 30: List living married people   
def livingmarried(filename):
    val=True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    name_list= []
    for fam in families:
        dad_id= fam['hid']
        mom_id= fam['wid']
        for check in individuals:
            if(dad_id==check['ID']):
                if(check['alive']==True):
                    dname=check['name']
                    dname=dname.split("/")
                    dfirst=dname[0]
                    dlast=dname[1]
                    name_list.append(dfirst+" "+dlast)
            if(mom_id==check['ID']):
                if(check['alive']==True):
                    mname=check['name']
                    mname=mname.split("/")
                    mfirst=mname[0]
                    mlast=mname[1]
                    name_list.append(mfirst+" "+mlast)
    for each in name_list:
        print(each)
    return val

#User Story 15: Fewer than 15 siblings
def fewerthan(filename):
    fval=True
    fdata = organize(filename)
    individuals = fdata[0]
    families = fdata[1]
    name_list= []
    for fam in families:
        children=fam['children']
        numofchildren=len(children)
        if(numofchildren>15):
            print("Family "+fam['ID']+" has more than 15 siblings")
            fval=False
    return fval

#User Story 21: Correct gender for roles
def genderroles(filename):
    val=True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    name_list= []
    for fam in families:
        dad_id= fam['hid']
        mom_id= fam['wid']
        for check in individuals:
            if(dad_id==check['ID']):
                if(check['gender']!='M'):
                    print("Family "+fam['ID']+" has an incorrect gender role for the Husband")
                    val=False
            if(mom_id==check['ID']):
                if(check['gender']!='F'):
                    print("Family "+fam['ID']+" has an incorrect gender role for the Wife")
                    val=False                
    return val


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

    #user story 22
    if(unique_indiv_id(fname) == True):
        print("Correct US22: All individual IDs are unique.")
    
    if(unique_family_id(fname) == True):
        print("Correct US22: All family IDs are unique.")

    #user story 42
    if(date_checker(fname) == True):
        print("Correct US42: All dates are legitimate")

    #khushi's user story 16
    if(male_lastname(fname) == True):
        print("Correct US16: All male names are the same")

    #khushi's user story 18
    if(sibs_nomarry(fname) == True):
        print("Correct US18: No siblings are married to each other")
    
    #khushi's user story 12
    if(parents_notold(fname) == True):
        print("Correct US12: Mother should be less than 60 years older than her children and father should be less than 80 years older than his children")

    #khushi's user story 30
    if(livingmarried(fname) == True):
        print("Correct US30: List living married people")

    #khushi's user story 15
    if(fewerthan(fname) == True):
        print("Correct US15: Each family has fewer than 15 siblings")

    #khushi's user story 21
    if(genderroles(fname) == True):
        print("Correct US21: Each family has correct gender roles for the Husband and Wife")

    return 

if __name__ == "__main__":
    main()