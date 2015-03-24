from PyCamellia import *

def steadyLinearInit(spaceDim, dims, numElements, polyOrder):
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
    return form

def addInflow(form, newInflow, newVelocity):
    form.addInflowCondition(newInflow, newVelocity)
    return form

def addOutflow(form, newOutflow):
    form.addOutflowCondition(newOutflow)
    return form

def energyPerCell(form):
    perCellError = form.solution().energyErrorPerCell()
    for cellID in perCellError:
        if perCellError[cellID] > .01:
            print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))
    return perCellError

def steadyLinearSolve(form):
    refinementNumber = 0
    form.solve()
    
    mesh = form.solution().mesh();
    
    energyError = form.solution().energyErrorTotal()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))

    return form

def steadyLinearRefine(form, threshold):
    threshold = .05
    while energyError > threshold and refinementNumber <= 8:
        form.refine()
        form.solve()
        energyError = form.solution().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    return form

def steadyLinearHRefine(form, threshold):
    threshold = .05
    while energyError > threshold and refinementNumber <= 8:
        form.hRefine()
        form.solve()
        energyError = form.solution().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    return form

def steadyLinearPRefine(form, threshold):
    while energyError > threshold and refinementNumber <= 8:
        form.pRefine()
        form.solve()
        energyError = form.solution().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    return form

def steadyLinearExport(form):
    exporter = HDF5Exporter(form.solution().mesh(), "steadyStokes", ".")
    exporter.exportSolution(form.solution(),0)
    return exporter


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

def transientLinearExport(form):
    exporter = HDF5Exporter(form.solution().mesh(), "transientStokes", ".")
    return exporter

def transientLinearSolve(form, totalTime, dt):
    exporter = HDF5Exporter(form.solution().mesh(), "transientStokes", ".")
    numTimeSteps = int(totalTime / dt)    
    for timeStepNumber in range(numTimeSteps):
        form.solve()
        exporter.exportSolution(form.solution(),form.getTime())
        form.takeTimeStep()
        print("Time step %i completed" % timeStepNumber)

    return form

def transientLinearRefine(form, threshold):
    while energyError > threshold and refinementNumber <= 8:
        form.refine()
        form.solve()
        energyError = form.solution().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    return form

def transientLinearHRefine(form, threshold):
    while energyError > threshold and refinementNumber <= 8:
        form.hRefine()
        form.solve()
        energyError = form.solution().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    return form

def transientLinearPRefine(form, threshold):
    while energyError > threshold and refinementNumber <= 8:
        form.PRefine()
        form.solve()
        energyError = form.solution().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    return form

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

def steadyNonlinearRefine(form, threshold, maxRefs, maxSteps):
    refinementNumber = 0
    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
    
    while energyError > threshold and refinementNumber <= maxRefs:
        form.refine()
        form = nonlinearSolve(form, maxSteps)
        energyError = form.solutionIncrement().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))

    return form

def steadyNonlinearHRefine(form, threshold, maxRefs, maxSteps):
    refinementNumber = 0
    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
    
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

def steadyNonlinearPRefine(form, threshold, maxRefs, maxSteps):
    refinementNumber = 0
    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
    
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

def steadyNonlinearExport(form):
    exporter = HDF5Exporter(form.solution().mesh(), "steadyNavierStokes", ".")
    exporter.exportSolution(form.solution(),0)
    return exporter


