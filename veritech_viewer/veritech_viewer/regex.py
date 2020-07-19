import re
trim = "2|8"
onedigit = re.search("^([0-9])$", trim)
twodigit = re.search("^([0-9])\)\(([0-9])$",trim)
orbrack = re.search("^(([0-9])\|)+",trim)
bracket_then_or = re.search("^([0-9])\)\((([0-9])\|*)+$", trim)
or_then_bracket = re.search("^(([0-9])\|*)+\)\(([0-9])$", trim)

if(onedigit):
    print("one " + trim)
elif(twodigit):
   print("two" + trim[0]+trim[3])

elif(bracket_then_or):
    print("here")
    tens_digit = trim[0]
    ones_digit = trim[3:].split("|")
    result = ""
    for i in range(0,len(ones_digit)):

        if(i != 0):
            result = result + " or "
        result = result+ tens_digit + ones_digit[i]
    print(result)
elif(or_then_bracket):
    print("or then")
    tens_digit = trim[:-3].split("|")
    ones_digit = trim[-1]
    print(tens_digit)
    print(ones_digit)
    result = ""
    for i in range(0,len(tens_digit)):
        if(i != 0):
            result = result + " or "
        result = result+ tens_digit[i] + ones_digit
    print(result)
elif (orbrack):
    print("orbrack")
    print(trim.replace("|", " or "))
else:
    print("else")
'''    
elif(or_then_bracket):
    tens_digit = trim[:-4].split("|")
    ones_digit = trim[:-2];
    for i in range(0,len(tens_digit)):
        if(i != 0):
            result = result + " or "
        result = result+ tens_digit[i] + ones_digit
    print(result)
    '''
