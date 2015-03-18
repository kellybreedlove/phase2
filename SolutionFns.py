from PyCamellia import *

def steadyLinearInit(spaceDim, Re, dims, numElements, polyOrder):
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
    form.addInflowCondition(newInflow,newVelocity)
    return form

def addOutflow(form, newOutflow):
    #form.addOutflowCondition()
    return form

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
        form.hRefine()
        form.solve()
        energyError = form.solution().energyErrorTotal()
        refinementNumber += 1
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
        print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    return form

def energyPerCell(form):
    perCellError = form.solution().energyErrorPerCell()
    for cellID in perCellError:
        if perCellError[cellID] > .01:
            print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))

def steadyLinearExport(form):
    exporter = HDF5Exporter(form.solution().mesh(), "steadyStokes", ".")
    exporter.exportSolution(form.solution(),0)


def transientLinearInit(spaceDim, Re, dims, numElements, polyOrder, dt):
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

def transientLinearSolve(form, totalTime, dt):
    exporter = HDF5Exporter(form.solution().mesh(), "transientStokes", ".")
    numTimeSteps = int(totalTime / dt)    
    for timeStepNumber in range(numTimeSteps):
        form.solve()
        exporter.exportSolution(form.solution(),form.getTime())
        form.takeTimeStep()
        print("Time step %i completed" % timeStepNumber)

    return form


