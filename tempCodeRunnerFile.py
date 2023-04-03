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
    if(date_helper(day,temp[1])):
        return date(year, month, day)
    else:
        return None