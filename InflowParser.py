from PyCamellia import *
delta_k = 1

def stringToFilter(inputstr):
    i = 0
    xFirst = True
    noComma = True
    for c in inputstr:
        if c == ',':
            noComma = False
            break
        i+=1
    if(noComma):
        if(inputstr[0] == 'x'):
            #print(inputstr[2:])
            xBounds = setXBoundary(inputstr)
            return xBounds
        elif(inputstr[0] == 'y'):
            #print(inputstr[2:])
            yBounds = setYBoundary(inputstr)
            return yBounds
        else:
            reject()
    arguments = inputstr.split(",")
    filters = []
    for argument in arguments:
        if argument[0] == 'x':
            filters.append(setXBoundary(argument))
        elif argument[0] == 'y':
            filters.append(setYBoundary(argument))
        else:
            reject()
    startingFilter = filters.pop() 
    for filter in filters:
        startingFilter and filter
    return startingFilter
    
            

def setXBoundary(inputstr):
    digits = float(inputstr[2:])
    #print(digits)
    c = inputstr[1]
    if not type(digits) == float: #Need to change to isLong or something similar
        reject()
    
    if c == '=':
        return SpatialFilter.matchingX(float(digits))
    elif c == '<':
        return SpatialFilter.lessThanX(float(digits))
    elif c == '>':
        return SpatialFilter.greaterThanX(float(digits))
    else:
        reject()
    




def setYBoundary(inputstr):
    digits = float(inputstr[2:])
    #print(type(digits))
    c = inputstr[1]
    if not type(digits) == float: #Need to change to isLong or something similar
        reject()
    if c == '=':
        return SpatialFilter.matchingY(float(digits))
    elif c == '<':
        return SpatialFilter.lessThanY(float(digits))
    elif c == '>':
        return SpatialFilter.greaterThanY(float(digits))
    else:
        reject()




def reject():
    raise ValueError
 
 
 
 


def stringToDims(inputstr):
    if not "x" in inputstr:
        reject()
    else:
        x = float(inputstr[:inputstr.index("x")])
        y = float(inputstr[inputstr.index("x")+1:])
        return [x,y]



def stringToElements(inputstr):
    if not "x" in inputstr:
        reject()
    else:
        x = int(inputstr[:inputstr.index("x")])
        y = int(inputstr[inputstr.index("x")+1:])
        return [x,y]
