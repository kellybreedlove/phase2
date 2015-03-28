from PyCamellia import *

def solve(data):
	spaceDim = 2
	useConformingTraces = True
	mu = 1.0
	x0 = [0.,0.]
	delta_k = 1
	dt = 0.1
	
	stokes = data["stokes"]
	if not stokes:
	    Re = data["reynolds"]
	transient = data["transient"]
	dims = data["meshDimensions"]
	numElements = data["numElements"]
	x0 = [0.,0.]
	polyOrder = data["polyOrder"]
	numInflows = data["numInflows"]
	inflowRegions = data["inflowRegions"]
	inflowX = data["inflowX"]
	inflowY = data["inflowY"]
	numOutflows = data["numOutflows"]
	outflowRegions = data["outflowRegions"]
	numWalls = data["numWalls"]
	wallRegions = data["wallRegions"]
	meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)

	
	if stokes:
	    if transient:
	        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu,transient,dt)
	        form.initializeSolution(meshTopo,polyOrder,delta_k)
	        timeRamp = TimeRamp.timeRamp(form.getTimeFunction(),1.0)
	    else:
	        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
	        form.initializeSolution(meshTopo,polyOrder,delta_k)
	else:
	    form = NavierStokesVGPFormulation(meshTopo,Re,polyOrder,delta_k)
	
	form.addZeroMeanPressureCondition()
	
	
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
	i = 0
	while i < numWalls:
	    form.addWallCondition(wallRegions[i])
	    i += 1
	    
	form.solve()
	print("Solving...")
	#print("Solve completed in __ minutes, __ seconds")
	return form
