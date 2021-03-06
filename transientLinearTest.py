from PyCamellia import *
from SolutionFns import *

spaceDim = 2
dims = [1.0,1.0]
numElements = [2,2]
polyOrder = 3
dt = 0.1
totalTime = 2.0

form = transientLinearInit(spaceDim, dims, numElements, polyOrder, dt)

topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
timeRamp = TimeRamp.timeRamp(form.getTimeFunction(),1.0)
x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)

zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)


form = addWall(form, notTopBoundary)
form = addInflow(form, topBoundary, timeRamp * topVelocity)

form = transientLinearSolve(form, totalTime, dt)
