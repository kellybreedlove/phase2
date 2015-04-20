from InputData import *
from SolveFormulation import *
from PyCamellia import *
import pickle
import copy

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

# nStokes, transient, or steady
def generateForm(kind):
    if kind == "nStokes":
        return generateFormNavierStokesSteady()
    if kind == "transient":
        return generateFormStokesTransient()
    if kind == "steady":
        return generateFormStokesSteady()
        
def generateFormStokesTransient():
    data = InputData(True)
    data.addVariable("transient", True)
    populateInputData(data)
    return solve(data)

def generateFormStokesSteady():
    data = InputData(True)
    data.addVariable("transient", False)
    populateInputData(data)
    return solve(data)

def generateFormNavierStokesSteady():
    data = InputData(False)
    data.addVariable("reynolds", re)
    data.addVariable("transient", False)
    populateInputData(data)
    return solve(data)


if __name__ == '__main__':
    form = generateForm("steady")
    form.save("testSave")

    data = InputData(True)
    data.addVariable("transient", False)
    data.addVariable("form", form)
    populateInputData(data)

    memento = data.createMemento()

    output = memento.get()
   
    del output["form"]
    del output["inflowRegions"]
    del output["inflowX"]
    del output["inflowY"]
    del output["outflowRegions"]
    del output["wallRegions"]
    for x in output:
        print x, ' : ', output[x]

    saveFile = open("testPickle", 'wb')
    pickle.dump(memento, saveFile)
    saveFile.close()


    loadFile = open("testPickle")
    memento = pickle.load(loadFile)
    loadFile.close()
    data.setMemento(memento)
			
    polyOrder = data.getVariable("polyOrder")
    if not data.getVariable("stokes"):
        spaceDim = 2
        reynolds = context.inputData.getVariable("reynolds")
        form = NavierStokesVGPFormulation("testSave", spaceDim, reynolds, polyOrder)
    else:
        form.initializeSolution("testSave", polyOrder)
			    
    data.setForm(form)
