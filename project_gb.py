from project import *
from datetime import date

# convert date string to date type
def date_format(string):
    if string is None:
        return None
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

# returns the diffence between 2 date strings
# in terms of months
def find_month_differance(start, end):
    dateStart = date_format(start)
    dateEnd = date_format(end)
    return (dateStart - dateEnd).days / 30.417

# user story 09: Birth Before Death of Parents
# check if birth's happen before death of the mother 
# and 9 months before the death of the father
def valid_birth(filename):
    data = organize(filename)
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
            if (wif['death'] != 'N/A' or hus['death'] != 'N/A'):
                for child in children:
                    if (wif['death'] != 'N/A'):
                        if(find_month_differance(child['birthday'],wif['death']) > 0):
                            validBirthdays = False
                            print('Error US09: ' + wif['name'] + "'s Death is before " + child['name'] + "'s Birth")
                    if (hus['death'] != 'N/A'):
                        if(find_month_differance(child['birthday'],hus['death']) > 9):
                            validBirthdays = False
                            print('Anomaly US09: ' + hus['name'] + "'s Death more than 9 months before " + child['name'] + "'s Birth")
    return(validBirthdays)

# user story 27 get persons age
def age(person):
    if(person['death'] == None):
        birthday = date_format(person['birthday'])
        return((date.today() - birthday) / 365)
    else:
        birthday = date_format(person['birthday'])
        death = date_format(person['death'])
        age = death - birthday
        if(age < 0):
            print('Error US27: ' + person['name'] + "'s Age is invalid")
        return((death - birthday) / 365)
