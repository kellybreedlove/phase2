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
    
    return form

# Begin Refine -------------------------------------------------------------

def steadyLinearHAutoRefine(form):
    print("Automatically refining in h...")
    form.hRefine()
    mesh = form.solution().mesh();
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)
    
    return form

def steadyLinearPAutoRefine(form):
    print("Automatically refining in p...")
    form.pRefine()
    mesh = form.solution().mesh();
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)
    
    return form

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
    print("Manually refining in p...")
    #cellList = cellList.split()          may be necessary for user input, but not for testing
    #cellList = map(int, cellList)
    mesh = form.solution().mesh();
    mesh.pRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)

# End Refine ---------------------------------------------------------------

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

def transientLinearSolve(form, totalTime, dt):
    exporter = HDF5Exporter(form.solution().mesh(), "transientStokes", ".")
    numTimeSteps = int(totalTime / dt)    
    for timeStepNumber in range(numTimeSteps):
        form.solve()
        exporter.exportSolution(form.solution(),form.getTime())
        form.takeTimeStep()
        print("Time step %i completed" % timeStepNumber)

def steadyNonlinearInit(spaceDim, re, dims, numElements, polyOrder):
    x0 = [0.,0.]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
    delta_k = 1

    form = NavierStokesVGPFormulation(meshTopo, re, polyOrder, delta_k)
    
    form.addZeroMeanPressureCondition()
    
    return form

#define a local method that will do the nonlinear iteration:
def nonlinearSolve(form, maxSteps):
    nonlinearThreshold = 1e-3
    normOfIncrement = 1
    stepNumber = 0
    while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
        form.solveAndAccumulate()
        normOfIncrement = form.L2NormSolutionIncrement()
        print("L^2 norm of increment: %0.3f" % normOfIncrement)
        stepNumber += 1
    return form

def steadyNonlinearSolve(form, maxSteps):
    refinementNumber = 0
    form = nonlinearSolve(form, maxSteps)
    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
    
    return form

def nonlinearHAutoRefine(form, maxSteps):
    threshold = 0.05
    maxRefs = 8
    refinementNumber = 0
    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()    
    while energyError > threshold and refinementNumber <= maxRefs:
        form.hRefine()
        form = nonlinearSolve(form, maxSteps)
        energyError = form.solutionIncrement().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
        
    return form

def nonlinearPAutoRefine(form, maxSteps):
    threshold = 0.05
    maxRefs = 8
    refinementNumber = 0
    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()   
    while energyError > threshold and refinementNumber <= maxRefs:
        form.pRefine()
        form = nonlinearSolve(form, maxSteps)
        energyError = form.solutionIncrement().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    
    return form

def nonlinearHManualRefine(form, maxSteps, cellList):
    refinementNumber = 0
    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    cellList = cellList.split()
    cellList = map(int, cellList)
    mesh.hRefine(cellList)
    form = nonlinearSolve(form, maxSteps)
    energyError = form.solutionIncrement().energyErrorTotal()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("Energy error: %0.3f" % (energyError))
    print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    
    return form

def nonlinearPManualRefine(form, maxSteps, cellList):
    refinementNumber = 0
    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    cellList = cellList.split()
    cellList = map(int, cellList)
    mesh.pRefine(cellList)
    form = nonlinearSolve(form, maxSteps)
    energyError = form.solutionIncrement().energyErrorTotal()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("Energy error: %0.3f" % (energyError))
    print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    
    return form

