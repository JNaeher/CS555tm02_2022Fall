from project import *

#returns the diffence between 2 date strings
#in terms of months
def find_month_differance(start, end):
    dateStart = date_format(start)
    dateEnd = date_format(end)
    return (dateStart - dateEnd).days / 30.48

#user story 09: Birth Before Death of Parents
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
            cbirths = []
            for person in individuals:
                if person['ID'] == hid:
                    hdeath = person['death']
                if person['ID'] == wid:
                    wdeath = person['death']
                for child in fam['children']:
                    if person['ID'] == child:
                        cbirths.append(person['birthday'])
            if (wdeath != 'N/A' or hdeath != 'N/A'):
                for birth in cbirths:
                    if (wdeath != 'N/A'):
                        if(find_month_differance(birth,wdeath) > 0):
                            validBirthdays = False
                            print('Error: Wife Death Before Child Birth')
                    if (hdeath != 'N/A'):
                        if(find_month_differance(birth,hdeath) > 9):
                            validBirthdays = False
                            print('Error: Husband Death more than 9 months before Child Birth')
    return(validBirthdays)

#user story 27: include individual ages

print(valid_birth("Project_test_gb.ged"))