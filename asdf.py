from PyCamellia import *
from Plotter import *
import unittest


spaceDim = 2
useConformingTraces = True
mu = 1.0
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
polyOrder = 3
delta_k = 1
topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)
refinementNumber = 0
refCellVertexPoints = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]]; 

print "Plot_energyError"
form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
form.initializeSolution(meshTopo,polyOrder,delta_k)
form.addZeroMeanPressureCondition()
form.addWallCondition(notTopBoundary)
form.addInflowCondition(topBoundary,topVelocity)
form.solve()
mesh = form.solution().mesh();

energyError = form.solution().energyErrorTotal()
elementCount = mesh.numActiveElements()
globalDofCount = mesh.numGlobalDofs()

activeCellIDs = mesh.getActiveCellIDs()

ceError = form.solution().energyErrorPerCell()
print array(ceError)
print len(activeCellIDs)
plotError(activeCellIDs,ceError,mesh,"Plot Energy Error")
form = None
