tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

file = open('test1.ged', 'r')
lines = file.readlines()
array = []

def exists(elem, list):
    for a in list:
        if(a == elem):
            return True
    return False

# gets rid of the end lines in the strings read from the file
for line in lines:
    array.append(line.strip())

for line in array:
    print("--> " + line)
    temp = line.split(" ", 2)
    if(len(temp) < 3): 
        print("<-- less than three arguments")
    elif(exists(temp[1], tags)):
        print("<-- " + temp[0] + "|" + temp[1] + "|Y|" + temp[2])
    else:
        if(temp[2] == 'INDI' or temp[2] == 'FAM'):
            print("<-- " + temp[0] + "|" + temp[1] + "|Y|" + temp[2])
        else:
            print("<-- " + temp[0] + "|" + temp[1] + "|N|" + temp[2])