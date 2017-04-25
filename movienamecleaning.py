import re


def cleanit(str):
    result = []
    l = re.split('[_.\s]',str)
    #print(l)
    flag = 0
    if re.match('^[a-zA-z]+',l[0]):
        flag = 1
    elif re.match('^[0-9]+',l[0]):
        flag = 2

    if flag == 1:
        for x in l:
            if not re.match(r'(^[a-zA-Z]+|^\d$)',x):
                break;
            result.append(x)
        return " ".join(result)

    if flag == 2:
        for x in l:
            if not re.match('^[0-9]+',x):
                break;
            result.append(x)
        return " ".join(result)
#print(cleanit('La La Land 2016'))
#print(not re.match(r'^\d$','2'))