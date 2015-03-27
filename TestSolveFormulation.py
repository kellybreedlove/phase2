from InflowParser import *
from ParseFunction import *
from InputData import *
from SolveFormulation import *

data = InputData(True)
data.addVariable("transient", True)
data.addVariable("mesh",MeshFactory.rectilinearMeshTopology([1.0,1.0],[2,2],[0.,0.]))
data.addVariable("polyOrder",  1)
data.addVariable("numInflows",  1)
data.addVariable("inflowRegions",  [stringToFilter("x<8")])
data.addVariable("inflowX",  [stringToFunction("4")])
data.addVariable("inflowY",  [stringToFunction("9")])
data.addVariable("numOutflows",  1)
data.addVariable("outflowRegions",  [stringToFilter("x<0")])
data.addVariable("numWalls",  1)
data.addVariable("wallRegions",  [stringToFilter("y>9")])

print solve(data.vars)
