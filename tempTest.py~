from PyCamellia import *
spaceDim = 2
useConformingTraces = True
mu = 1.0
form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
polyOrder = 3
delta_k = 1

form.initializeSolution(meshTopo,polyOrder,delta_k)

form.addZeroMeanPressureCondition()

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

refinementNumber = 0
form.solve()

mesh = form.solution().mesh();

energyError = form.solution().energyErrorTotal()
elementCount = mesh.numActiveElements()
globalDofCount = mesh.numGlobalDofs()
print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))

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

# print out per-cell energy error for cells with energy error > 0.01:
perCellError = form.solution().energyErrorPerCell()
for cellID in perCellError:
  if perCellError[cellID] > .01:
    print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))

exporter = HDF5Exporter(form.solution().mesh(), "steadyStokes", ".")
exporter.exportSolution(form.solution(),0)

transient = True
dt = 0.1
totalTime = 2.0
numTimeSteps = int(totalTime / dt)
transientForm = StokesVGPFormulation(spaceDim,useConformingTraces,mu,transient,dt)

timeRamp = TimeRamp.timeRamp(transientForm.getTimeFunction(),1.0)

transientForm.initializeSolution(meshTopo,polyOrder,delta_k)

transientForm.addZeroMeanPressureCondition()
transientForm.addWallCondition(notTopBoundary)
transientForm.addInflowCondition(topBoundary,timeRamp * topVelocity)

transientExporter = HDF5Exporter(transientForm.solution().mesh(), "transientStokes", ".")

for timeStepNumber in range(numTimeSteps):
  transientForm.solve()
  transientExporter.exportSolution(transientForm.solution(),transientForm.getTime())
  transientForm.takeTimeStep()
  print("Time step %i completed" % timeStepNumber)

