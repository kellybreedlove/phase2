from PyCamellia import *
from SolutionFns import *

spaceDim = 2
Re = 800
dims = [1.0,1.0]
numElements = [2,2]
polyOrder = 3

form = steadyLinearInit(spaceDim, Re, dims, numElements, polyOrder)

topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)

x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)

zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)

form.addWallCondition(notTopBoundary)
form.addInflowCondition(topBoundary,topVelocity)

form = steadyLinearAddWall(form, notTopBoundary)
form = steadyLinearAddInflow(form, topBoundary, topVelocity)

form = steadyLinearSolve(form)
