from unittest import skip
from prettytable import PrettyTable
from datetime import date
from dateutil import relativedelta
import sys

#reminder: output into a file

# f = open("output.txt", 'w')
# sys.stdout = f

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

# convert date string to date type

def string_to_date(string): 
    x = 0
    if string is None:
        return None
    temp = string.split(" ", 2)
    if(len(temp) == 3):
        day = int(temp[0])
        year = int(temp[2])
        month = 0
        x = 1
    else:
        year = int(temp[1])
        month = 0
        day = 1
    
    if(temp[x] == 'JAN'):
        month = 1
    if(temp[x] == 'FEB'):
        month = 2
    if(temp[x] == 'MAR'):
        month = 3
    if(temp[x] == 'APR'):  
        month = 4
    if(temp[x] == 'MAY'):
        month = 5
    if(temp[x] == 'JUN'):
        month = 6
    if(temp[x] == 'JUL'):
        month = 7
    if(temp[x] == 'AUG'):
        month = 8
    if(temp[x] == 'SEP'):
        month = 9
    if(temp[x] == 'OCT'):
        month = 10
    if(temp[x] == 'NOV'):
        month = 11 
    if(temp[x] == 'DEC'):
        month = 12
    if(date_helper(day,temp[x])):
        return date(year, month, day)
    else:
        return None

#user story #6

#given an id, return the death associated with it
def death_finder(individuals,id):
    for individual in individuals:
        if(individual['ID'] == id):
            return individual['death']

#check if divorce occurs before death of both individuals
def divorce_before_death(filename):
    valid = True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    for family in families:
        hus_id = family['hid']
        hus_death_str = death_finder(individuals,hus_id)
        hus_death = string_to_date(hus_death_str)
        wife_id = family['wid']
        wife_death_str = death_finder(individuals,wife_id)
        wife_death = string_to_date(wife_death_str)
        div_date_str = family['divorced']
        div_date = string_to_date(div_date_str)
        if(div_date == None):
            continue
        elif((hus_death == None) and (wife_death == None)):
            continue
        elif((hus_death != None) and (wife_death != None) and (hus_death < div_date) and (wife_death < div_date)):
            valid = False
            print("Error US06: Individual ID's (" + hus_id + "), (" + wife_id + ") deaths occur before the divorce date.")
        elif((hus_death != None) and (hus_death < div_date)):
            valid = False
            print("Error US06: Individual ID (" + hus_id + ") death occurs before the divorce date.")
        elif((wife_death != None) and (wife_death < div_date)):
            valid = False
            print("Error US06: Individual ID (" + wife_id + ") death occur before the divorce date.")
    return valid


#user story 10: marriage after 14

#given an id, return the birthday associated with it
def birthday_finder(individuals,id):
    for individual in individuals:
        if(individual['ID'] == id):
            return individual['birthday']
        
#given an id, return the deathday associated with it
def deathday_finder(individuals,id):
    for individual in individuals:
        if(individual['ID'] == id):
            return individual['death']

#check if marriage occurs before either individual turns 14 years old
def marriage_after_14(filename):
    valid = True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    for family in families:
        hus_id = family['hid']
        hus_birthday_str = birthday_finder(individuals,hus_id)
        hus_birthday = string_to_date(hus_birthday_str)
        hus_14 = hus_birthday.replace(year=hus_birthday.year+14)
        wife_id = family['wid']
        wife_birthday_str = birthday_finder(individuals,wife_id)
        wife_birthday = string_to_date(wife_birthday_str)
        wife_14 = wife_birthday.replace(year=wife_birthday.year+14)
        marriage_date_str = family['married']
        marriage_date = string_to_date(marriage_date_str)

        if(marriage_date == None):
            continue
        elif((hus_14 > marriage_date) and (wife_14 > marriage_date)):
            valid = False
            print("Error US10: Marriage occurs before individual ID's (" + wife_id + "), (" + hus_id + ") turned 14 years old.")
        elif(hus_14 > marriage_date):
            valid = False
            print("Error US10: Marriage occurs before individual ID (" + hus_id + ") turned 14 years old.")
        elif(wife_14 > marriage_date):
            valid = False
            print("Error US10: Marriage occurs before individual ID (" + wife_id + ") turned 14 years old.")
    return valid

#user story 25

#checks that no more than one child with the same name and birth date appears in a family
def unique_firstnames_in_fam(filename):
    valid = True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    for family in families:
        names = []
        birthdays = []
        children = family['children']
        for child in children:
            childname = ''
            childbirthday = ''
            childid = ''
            for check in individuals:
                if((child == check['ID'])):
                    childname = check['name']
                    childname = childname.split(" ")
                    childfirstname = childname[0]
                    childbirthday = birthday_finder(individuals, check['ID'])
                    childid = check['ID']
            length = len(names)
            for i in range(length):
                if(childfirstname == names[i] and childbirthday == birthdays[i]):
                    valid = False
                    print("Error US25: Child with ID " + childid + " shares a first name and birthday with one or more of their siblings.")
            names.append(childfirstname)
            birthdays.append(childbirthday)
    return valid

def birth_after_marriage(filename):
    valid = True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    for family in families:
        marriage_date = string_to_date(family['married'])
        children = family['children']
        for child in children:
            childbirthday = ''
            childid = ''
            for check in individuals:
                if((child == check['ID'])):
                    childbirthday = string_to_date(birthday_finder(individuals, check['ID']))
                    childid = check['ID']
            if(marriage_date != None and marriage_date > childbirthday):
                valid = False
                print("Error US08: Child with ID " + childid + " has a birthday before parent's marriage.")
    return valid

def sibling_spacing(filename):
    valid = True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    for family in families:
        birthdays = []
        children = family['children']
        for child in children:
            for check in individuals:
                if((child == check['ID'])):
                    birthdays.append(string_to_date(birthday_finder(individuals, check['ID'])))
        # iterate pairwise over birthdays
        for i in range(0, len(birthdays) - 2):
            delta = relativedelta.relativedelta(birthdays[i], birthdays[i+1])
            if(abs(delta.months) <= 8 or (abs(delta.months) < 1 and abs(delta.days < 2))):
                valid = False
                print("Error US13: Children with IDs " + children[i] + " and " + children[i] + " have a birthday < 8 months apart and are not twins.")

    return valid

#user story 23: unique name and birth date
def unique_name_id(filename):
    valid = True
    data = organize(filename)
    individuals = data[0]
    names = []
    birthdays = []
    for individual in individuals:
        indiv_name = individual['name']
        indiv_bday = string_to_date(birthday_finder(individuals, individual['ID']))
        for i in range(len(names)):
            if(indiv_name == names[i] and indiv_bday == birthdays[i]):
                valid = False
                print("Error US23: Individual with ID " + individual['ID'] + " shares a name and birthday with one or more individuals.")
        names.append(indiv_name)
        birthdays.append(indiv_bday)
    return valid

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

# user story 7: less than 150 years old
def less_than_150(filename):
    valid = True
    data = organize(filename)
    individuals = data[0]
    for indiv in individuals:
        birthday = string_to_date(birthday_finder(individuals, indiv['ID']))
        deathday = string_to_date(death_finder(individuals, indiv['ID']))
        if(deathday != None):
            difference = deathday - birthday
            difference_in_years = (difference.days + difference.seconds/86400)/365.2425
            if(difference_in_years >= 150):
                valid = False
                print("Error US07: Individual " + "(" + indiv['ID'] + ") died more than 150 years past their birth date.")
    return valid

def are_couple(families, id1, id2):
    for family in families:
        wid = family['wid']
        hid = family['hid']
        if ((wid == id1 and hid == id2) or (wid == id2 and hid == id1)):
            return True
    return False

# user story 17: no marriage to descendants
def no_marry_desc(filename):
    valid = True
    data = organize(filename)
    families = data[1]
    for family in families:
        wid = family['wid']
        hid = family['hid']
        children = family['children']
        for child in children:
            if(are_couple(families, wid, child)):
                valid = False
                print("Error US17: Individual " + "(" + wid + ") married a descendant.")
            elif(are_couple(families, hid, child)):
                valid = False
                print("Error US17: Individual " + "(" + hid + ") married a descendant.")
    return valid
    
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
# returns the diffence between 2 date strings
# in terms of months
def find_month_differance(start, end):
    dateStart = string_to_date(start)
    dateEnd = string_to_date(end)
    if dateStart == None or dateEnd == None:
        return None
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
                        monthDif = find_month_differance(child['birthday'],wif['death'])
                        if(monthDif == None):
                            validBirthdays = False
                            print("Error US09: Invalid Data")
                        elif(monthDif > 0):
                            validBirthdays = False
                            print('Error US09: ' + wif['name'] + "'s Death is before " + child['name'] + "'s Birth")
                    if (hus['death'] != None):
                        monthDif = find_month_differance(child['birthday'],hus['death'])
                        if(monthDif == None):
                            validBirthdays = False
                            print("Error US09: Invalid Data")
                        elif(monthDif > 9):
                            validBirthdays = False
                            print('Anomaly US09: ' + hus['name'] + "'s Death is more than 9 months before " + child['name'] + "'s Birth")
    return(validBirthdays)

# user story 27 get persons age
def get_age(person):
    if(person['birthday'] == None):
        return -1
    elif(person['death'] == None):
        birthday = string_to_date(person['birthday'])
        if(birthday == None):
            return -1
        age = int((date.today() - birthday).days / 365)
        return age
    else:
        birthday = string_to_date(person['birthday'])
        if(birthday == None):
            return -1
        death = string_to_date(person['death'])
        if(death == None):
            return -1
        age = int((death - birthday).days / 365)
        return age

#user story 29, list deceased
def list_deceased(filename):
    data = organize(filename)
    individuals = data[0]
    temp = True
    for person in individuals:
        if(person['alive'] == False):
            print("US 29: " + person['name'] + " is deceased.")
            temp = False
    return temp

#user story 01, dates after current date
def dates_after_current(filename):
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    temp = True
    current_date = date.today()
    for person in individuals:
        birth = string_to_date(person['birthday'])
        death = string_to_date(person['death'])
        if(birth is not None):
            if(birth > current_date):
                temp = False
                print("Anomoly US01: " + person['name'] + " has a birthday after today's date.")
        if(death is not None):
            if(death > current_date):
                temp = False
                print("Anomoly US01: " + person['name'] + " has a death date after today's date.")

    for family in families:
        marriage = string_to_date(family['married'])
        divorced = string_to_date(family['divorced'])
        if(marriage is not None):
            if(marriage > current_date):
                temp = False
                print("Anomoly US01: " + family['ID'] + " has a marriage date after today's date.")

        if(divorced is not None):
            if(divorced > current_date):
                temp = False
                print("Anomoly US01: " + family['ID'] + " has a divorce date after today's date.")

    return temp

# BAD SMELL CODE DUPLICATE CODE FOR USER STORY 35 and 36
# user story 35 and 36
def recent_births_and_deaths(data):
    individuals = data[0]
    recentBirths = []
    recentDeaths = []
    for indiv in  individuals:
        birthday = string_to_date(birthday_finder(individuals , indiv['ID']))
        if(birthday != None and (date.today() - birthday).days <= 30):
            recentBirths.append(indiv)
        deathday = string_to_date(deathday_finder(individuals , indiv['ID']))
        if(deathday != None and (date.today() - deathday).days <= 30):
            recentDeaths.append(indiv)
    return([recentBirths,recentDeaths])

#User Story 21: Correct gender for role
def genderroles(filename):
    val=True
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    ret_val = True
    for fam in families:
        wid = fam['wid']
        hid = fam['hid']
        mar_date = string_to_date(fam['married'])
        if mar_date is None:
            continue
        wife = next(person for person in individuals if person['ID'] == wid)
        husband = next(person for person in individuals if person['ID'] == hid)
        wife_birth = string_to_date(wife['birthday'])
        husb_birth = string_to_date(husband['birthday'])
        if(wife_birth > mar_date):
            ret_val = False
            print("Anomoly US02: " + wife['name'] + " was born after they were married")
        if(husb_birth > mar_date):
            ret_val = False
            print("Anomoly US02: " + husband['name'] + " was born after they were married")
    return ret_val

# user story 02, birth before marriage
def birth_before_marriage(filename):
    data = organize(filename)
    individuals = data[0]
    families = data[1]
    ret_val = True
    for fam in families:
        wid = fam['wid']
        hid = fam['hid']
        mar_date = string_to_date(fam['married'])
        if mar_date is None:
            continue
        wife = next(person for person in individuals if person['ID'] == wid)
        husband = next(person for person in individuals if person['ID'] == hid)
        wife_birth = string_to_date(wife['birthday'])
        husb_birth = string_to_date(husband['birthday'])
        if(wife_birth > mar_date):
            ret_val = False
            print("Anomoly US02: " + wife['name'] + " was born after they were married")
        if(husb_birth > mar_date):
            ret_val = False
            print("Anomoly US02: " + husband['name'] + " was born after they were married")
    return ret_val

# user story 03
def birth_before_death(filename):
    data = organize(filename)
    individuals = data[0]
    ret_val = True
    for person in individuals:
        if person['alive'] == False:
            birth = string_to_date(person['birthday'])
            death = string_to_date(person['death'])
            if(birth > death):
                ret_val = False
                print("Anomoly US03: " + person['name'] + " has a birthday after their death.")
    return ret_val

def get_individual(individuals, id):
    for indiv in individuals:
        if indiv['ID'] == id:
            return indiv
    return None

# user story 31
# List living single
def single_and_over_30(data):
    individuals = data[0]
    single_indivis = []
    for indiv in individuals:
        if indiv['age'] > 30 and indiv['spouse'] == None:
            single_indivis.append(indiv)
    return single_indivis

# user story 34
# List large age differences
def large_age_marriage_difference(data):
    individuals = data[0]
    families = data[1]
    large_couples = []
    for fam in families:
        marriage_date = fam['married']
        if marriage_date != None:
            marriage = string_to_date(marriage_date)
            hus = get_individual(individuals, fam['hid'])
            wif = get_individual(individuals, fam['wid'])
            hus_marriage_age = (marriage - string_to_date(hus['birthday'])).days / 365
            wif_marriage_age = (marriage - string_to_date(wif['birthday'])).days / 365
            if hus_marriage_age > wif_marriage_age :
                if hus_marriage_age > 2 * wif_marriage_age :
                    large_couples.append[fam]
            else :
                if 2 * hus_marriage_age < wif_marriage_age :
                    large_couples.append[fam]
    return large_couples

def main():
    #getting data from the file given from command line

    fname = sys.argv[1]
    data = organize(fname)
    individuals = data[0]
    families = data[1]

    #prints the tables
    printIndividuals(individuals, families)
    printFamilies(individuals, families)

    #user story 35
    recent_birth__and_death = recent_births_and_deaths(data)
    if(len(recent_birth__and_death[0]) > 0):
        print("\nRecent Births in the last 30 days:")
        printIndividuals(recent_birth__and_death[0], families)
    else:
        print("\nNo Recent Births in the last 30 days:")
    
    #user story 36
    if(len(recent_birth__and_death[1]) > 0):
        print("\nRecent Deaths in the last 30 days:")
        printIndividuals(recent_birth__and_death[1], families)
    else:
        print("\nNo Recent Deaths in the last 30 days:")

    #user story 31
    single_and_over_30_data = single_and_over_30(data)
    if(len(single_and_over_30_data) > 0):
        print("\nFamily Members who are over 30 and haven't been married: ")
        printIndividuals(single_and_over_30_data, families)
    else:
        print("\nNo Family Members who are over 30 and haven't been married:")

    #user story 34
    double_marriage_age = large_age_marriage_difference(data)
    if(len(double_marriage_age) > 0):
        print("\nMarriages in which one couple is twice the age of the other: ")
        printFamilies(individuals, single_and_over_30_data)
    else:
        print("\nNo Marriages in which one couple is twice the age of the other: ")

    #does the checking from the user stories

    #user story 07
    if(less_than_150(fname) == True):
        print("Correct US07: All dead individuals died less than 150 years after their birth date.")

    #user story 09
    if(valid_birth(data) == True):
        print("Correct US09: All Children born while parents where alive")

    #user story 17
    if(no_marry_desc(fname) == True):
        print("Correct US17: No marriages occur between parents and descendants.")

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

    #khushi's user story 21 sprint 3
    if(genderroles(fname) == True):
        print("Correct US21: Each family has correct gender roles for the Husband and Wife")

    #user story 02
    if(birth_before_marriage(fname) == True):
        print("US 02: All marriages occured after those married were born")

    #user story 03
    if(birth_before_death(fname) == True):
        print("US03: All individuals have a birthday before their death")
    
    # f.close()
    return 


if __name__ == "__main__":
    main()