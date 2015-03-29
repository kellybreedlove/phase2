from PyCamellia import *
from time import *

spaceDim = 2 # always two because we aren't handling anything 3D

def steadyLinearInit(dims, numElements, polyOrder):
    x0 = [0.,0.]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
    delta_k = 1
    mu = 1.0
    useConformingTraces = True
    
    form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
    form.initializeSolution(meshTopo,polyOrder,delta_k)
    form.addZeroMeanPressureCondition()

    return form

def addWall(form, newWall):
    form.addWallCondition(newWall)

def addInflow(form, newInflow, newVelocity):
    form.addInflowCondition(newInflow, newVelocity)

def addOutflow(form, newOutflow):
    form.addOutflowCondition(newOutflow)

def energyPerCell(form):
    perCellError = form.solution().energyErrorPerCell()
    for cellID in perCellError:
        if perCellError[cellID] > .01:
            print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))
    return perCellError

def steadyLinearSolve(form):
    print("Solving..."),
    start = time()
    form.solve()
    mesh = form.solution().mesh();    
    energyError = form.solution().energyErrorTotal()
    end = time()
    mins = (end - start) / 60
    secs = (end - start) % 60
    print("Solve completed in %i minute, %i seconds." % (mins, secs))
    print("Energy error is %0.3f" % (energyError))

# -------------------------------------------------------------

def steadyLinearHAutoRefine(form):
    print("Automatically refining in h..."),
    form.hRefine()
    mesh = form.solution().mesh();
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)

def steadyLinearPAutoRefine(form):
    print("Automatically refining in p..."),
    form.pRefine()
    mesh = form.solution().mesh();
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)

def linearHManualRefine(form,cellList):
    print("Manually refining in h..."),
    #cellList = cellList.split()          may be necessary for user input, but not for testing
    #cellList = map(int, cellList)
    mesh = form.solution().mesh();
    mesh.hRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)

def linearPManualRefine(form, cellList):
    print("Manually refining in p..."),
    #cellList = cellList.split()          may be necessary for user input, but not for testing
    #cellList = map(int, cellList)
    mesh = form.solution().mesh();
    mesh.pRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)

# ---------------------------------------------------------------

def transientLinearInit(spaceDim, dims, numElements, polyOrder, dt):
    transient = True
    x0 = [0.,0.]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
    delta_k = 1
    mu = 1.0
    useConformingTraces = True

    form = StokesVGPFormulation(spaceDim, useConformingTraces, mu, transient, dt)    
    form.initializeSolution(meshTopo, polyOrder, delta_k)
    form.addZeroMeanPressureCondition()

    return form

def transientLinearSolve(form):
    print("Solving...")
    start = time()

    dt = 0.1
    totalTime = 2.0
    numTimeSteps = int(totalTime / dt)    
    for timeStepNumber in range(numTimeSteps):
        form.solve()
        form.takeTimeStep()
        print("Time step %i completed" % timeStepNumber)

    mesh = form.solution().mesh()
    energyError = form.solution().energyErrorTotal()
    end = time()
    mins = (end - start) / 60
    secs = (end - start) % 60
    print("Solve completed in %i minute, %i seconds." % (mins, secs))
    print("Energy error is %0.3f" % (energyError))

# ---------------------------------------------------------------

def steadyNonlinearInit(spaceDim, re, dims, numElements, polyOrder):
    x0 = [0.,0.]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
    delta_k = 1
    form = NavierStokesVGPFormulation(meshTopo, re, polyOrder, delta_k)
    form.addZeroMeanPressureCondition()
    return form

# helper method
def nonlinearSolve(form):
    maxSteps = 10
    normOfIncrement = 1
    stepNumber = 0
    nonlinearThreshold = 1e-3
    while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
        form.solveAndAccumulate()
        normOfIncrement = form.L2NormSolutionIncrement()
        print("L^2 norm of increment: %0.3f" % normOfIncrement)
        stepNumber += 1

def steadyNonlinearSolve(form):
    print("Solving...")
    start = time()

    nonlinearSolve(form)

    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    end = time()
    mins = (end - start) / 60
    secs = (end - start) % 60
    print("Solve completed in %i minute, %i seconds." % (mins, secs))
    print("Energy error is %0.3f" % (energyError))

# -------------------------------------------------------------

def nonlinearHAutoRefine(form):
    print("Automatically refining in h..."),
    form.hRefine()
    mesh = form.solution().mesh()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyNonlinearSolve(form)

def nonlinearPAutoRefine(form):
    print("Automatically refining in p..."),
    form.pRefine()
    mesh = form.solution().mesh()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyNonlinearSolve(form)

def nonlinearHManualRefine(form, cellList):
    print("Manually refining in h..."),
    #cellList = cellList.split()          may be necessary for user input, but not for testing
    #cellList = map(int, cellList)
    mesh = form.solution().mesh()
    mesh.hRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyNonlinearSolve(form)

def nonlinearPManualRefine(form, cellList):
    print("Manually refining in p..."),
    #cellList = cellList.split()          may be necessary for user input, but not for testing
    #cellList = map(int, cellList)
    mesh = form.solution().mesh()
    mesh.pRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyNonlinearSolve(form)
