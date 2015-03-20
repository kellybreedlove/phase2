String input //contains the input for the condition


def 

i = 0
xFirst = True
for c in input:
    if c == ',':
        break
    i++
firstHalf = input[:i]
secondHalf = input[i+1:] #add error handling in case there is no comma

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
    if !xFirst:
        reject()
    yBounds = setYBoundary(secondHalf)
else:
    reject()






def setXBoundary(input):
    digits = input[2:]
    c = input[1]
    if !digits.isdigit(): #Need to change to isLong or something similar
        reject()
    if c == '=':
        return SpatialFilter.matchingX(digits)
    elif c == '<':
        return SpatialFilter.lessThanX(digits)
    elif c == '>':
        return SpatialFilter.greaterThanX(digits)
    else :
        break
    




def setYBoundary(input):
    digits = input[2:]
    c = input[1]
    if !digits.isdigit(): #Need to change to isLong or something similar
        reject()
    if c == '=':
        return SpatialFilter.matchingY(digits)
    elif c == '<':
        return SpatialFilter.lessThanY(digits)
    elif c == '>':
        return SpatialFilter.greaterThanY(digits)
    else :
        break




def reject():
    raise ValueError("String not acceptable")
