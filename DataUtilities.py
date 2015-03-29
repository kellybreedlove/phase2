from InputData import *
from SolveFormulation import *

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

def generateFor
