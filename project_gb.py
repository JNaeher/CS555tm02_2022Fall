from project import *

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
