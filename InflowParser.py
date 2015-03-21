#String inputstr contains the input for the condition


def parse():
    i = 0
    xFirst = True
    for c in inputstr:
        if c == ',':
         break
        i+=1
    firstHalf = inputstr[:i]
    secondHalf = inputstr[i+1:] #add error handling in case there is no comma

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






def setXBoundary(inputstr):
    digits = inputstr[2:]
    c = inputstr[1]
    if not digits.isdigit(): #Need to change to isLong or something similar
        reject()
    if c == '=':
        return SpatialFilter.matchingX(digits)
    elif c == '<':
        return SpatialFilter.lessThanX(digits)
    elif c == '>':
        return SpatialFilter.greaterThanX(digits)
    else:
        reject()
    




def setYBoundary(inputstr):
    digits = inputstr[2:]
    c = inputstr[1]
    if not digits.isdigit(): #Need to change to isLong or something similar
        reject()
    if c == '=':
        return SpatialFilter.matchingY(digits)
    elif c == '<':
        return SpatialFilter.lessThanY(digits)
    elif c == '>':
        return SpatialFilter.greaterThanY(digits)
    else:
        reject()




def reject():
    raise ValueError("String not acceptable")
