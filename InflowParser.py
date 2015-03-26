#String inputstr contains the input for the condition
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
        if(inputstr[0] == 'x' and inputstr[1] == '='):
            #print(inputstr[2:])
            xBounds = setXBoundary(inputstr)
            return xBounds
        elif(inputstr[0] == 'y' and inputstr[1] == '='):
            #print(inputstr[2:])
            yBounds = setYBoundary(inputstr)
            return yBounds
        else:
            reject()
    else:
        firstHalf = inputstr[:i]
        print('FirstHalf: %s' % firstHalf)
        secondHalf = inputstr[i+1:] #add error handling in case there is no comma
        print('SecondHalf: %s' % secondHalf)
        c = firstHalf[0]
        if c == 'x':
            xBounds = setXBoundary(firstHalf)
        elif c == 'y':
            yBounds = setYBoundary(firstHalf)
            xFirst = False
        else:
            reject()
        c = secondHalf[0]
        if c == 'x':
            if xFirst:
                reject()
            xBounds = setXBoundary(secondHalf)
        elif c == 'y':
            if not xFirst:
                reject()
            yBounds = setYBoundary(secondHalf)
        else:
            reject()
        
        return xBounds and yBounds






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
