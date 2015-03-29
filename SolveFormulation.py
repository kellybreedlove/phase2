from PyCamellia import *
from SolutionFns import *

def solve(data):
	spaceDim = 2
	useConformingTraces = True
	mu = 1.0
	x0 = [0.,0.]
	delta_k = 1
	dt = 0.1
	
	stokes = data.getVariable("stokes")
	if not stokes:
	    Re = data.getVariable("reynolds")
	transient = data.getVariable("transient")
	dims = data.getVariable("meshDimensions")
	numElements = data.getVariable("numElements")
	x0 = [0.,0.]
	polyOrder = data.getVariable("polyOrder")
	numInflows = data.getVariable("numInflows")
	inflowRegions = data.getVariable("inflowRegions")
	inflowX = data.getVariable("inflowX")
	inflowY = data.getVariable("inflowY")
	numOutflows = data.getVariable("numOutflows")
	outflowRegions = data.getVariable("outflowRegions")
	numWalls = data.getVariable("numWalls")
	wallRegions = data.getVariable("wallRegions")
	meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)


	transientLinear = False
	steadyLinear = False
	steadyNonlinear = False

	if stokes:
	    if transient:
	        transientLinear = True
		form = transientLinearInit(spaceDim, dims, numElements, polyOrder, dt)
	        timeRamp = TimeRamp.timeRamp(form.getTimeFunction(),1.0)
	    else:
		steadyLinear = True
		form = steadyLinearInit(dims, numElements, polyOrder)
	else:
	    steadyNonlinear = True
	    form = steadyNonlinearInit(spaceDim, Re, dims, numElements, polyOrder)
	
	i = 0
	while i < numInflows:
	    inflowFunction = Function.vectorize(inflowX[i], inflowY[i])
	    if transient:
	        form.addInflowCondition(inflowRegions[i], timeRamp*inflowFunction)
	    else:
	        form.addInflowCondition(inflowRegions[i], inflowFunction)
	    i += 1
	    
	i = 0
	while i < numOutflows:
	    form.addOutflowCondition(outflowRegions[i])
	    i += 1  
	i = 1
	for i in wallRegions:
	    form.addWallCondition(i)
	

	if transientLinear:
		transientLinearSolve(form)
	elif steadyLinear:
		steadyLinearSolve(form)
	elif steadyNonlinear:
		steadyNonlinearSolve(form)

		
	return form 
