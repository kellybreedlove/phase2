from ConditionParser import *
from ParseFunction import *
from InputData import *
from SolveFormulation import *
import unittest

spaceDim = 2
useConformingTraces = True
mu = 1.0
x0 = [0.,0.]
delta_k = 1
dt = 0.1
x0 = [0.,0.]

re = 1000.0
dims = [1.0,1.0]
numElements = [2,2]
polyOrder = 1
inflowRegion = stringToFilter("x<8")
inflowX = stringToFunction("4")
inflowY = stringToFunction("9")
outflowRegion = stringToFilter("x<0")
wallRegion = stringToFilter("y>9")

# everything but stokes, reynolds, and transient
def populateInputData(data):
    data.addVariable("meshDimensions", dims)
    data.addVariable("numElements", numElements)
    data.addVariable("polyOrder",  polyOrder)
    data.addVariable("numInflows",  1)
    data.addVariable("inflowRegions",  [inflowRegion])
    data.addVariable("inflowX",  [inflowX])
    data.addVariable("inflowY",  [inflowY])
    data.addVariable("numOutflows",  1)
    data.addVariable("outflowRegions",  [outflowRegion])
    data.addVariable("numWalls",  1)
    data.addVariable("wallRegions",  [wallRegion])


class TestSolveFormulation(unittest.TestCase):
    
    """Test Solve Stokes Transient"""
    def test_solveStokesTransient(self):
        data = InputData(True)
        data.addVariable("transient", True)
        populateInputData(data)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)

        form = solve(data)

        foo = transientLinearInit(spaceDim, dims, numElements, polyOrder, dt)
	timeRamp = TimeRamp.timeRamp(foo.getTimeFunction(),1.0)
        inflowFunction = Function.vectorize(inflowX, inflowY)
        foo.addInflowCondition(inflowRegion, timeRamp*inflowFunction)
        foo.addOutflowCondition(outflowRegion)
        foo.addWallCondition(wallRegion)
        transientLinearSolve(form)
                
    
    """Test Solve Stokes Steady"""
    def test_solveStokesSteady(self):
        data = InputData(True)
        data.addVariable("transient", False)
        populateInputData(data)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
        
        form = solve(data)

        foo = steadyLinearInit(dims, numElements, polyOrder)
        inflowFunction = Function.vectorize(inflowX, inflowY)
        foo.addInflowCondition(inflowRegion, inflowFunction)
        foo.addOutflowCondition(outflowRegion)
        foo.addWallCondition(wallRegion)
        steadyLinearSolve(form)

    
    """Test Solve NavierStokes Steady"""
    def test_solveNavierStokesSteady(self):
        data = InputData(False)
        data.addVariable("reynolds", re)
        data.addVariable("transient", False)
        populateInputData(data)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
        
        form = solve(data)

        foo = steadyNonlinearInit(spaceDim, re, dims, numElements, polyOrder)
        inflowFunction = Function.vectorize(inflowX, inflowY)
        foo.addInflowCondition(inflowRegion, inflowFunction)
        foo.addOutflowCondition(outflowRegion)
        foo.addWallCondition(wallRegion)
        steadyNonlinearSolve(form)


    if __name__ == '__main__':
        unittest.main()




