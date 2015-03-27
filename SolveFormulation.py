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
	meshTopo = data.getVariable("mesh")
	polyOrder = data.getVariable("polyOrder")
	numInflows = data.getVariable("numInflows")
	inflowRegions = data.getVariable("inflowRegions")
	inflowX = data.getVariable("inflowX")
	inflowY = data.getVariable("inflowY")
	numOutflows = data.getVariable("numOutflows")
	outflowRegions = data.getVariable("outflowRegions")
	numWalls = data.getVariable("numWalls")
	wallRegions = data.getVariable("wallRegions")
	
	
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
	
	inflowFunction = Function.vectorize(inflowX[i], inflowY[i])
	
	i = 0
	while i < numInflows:
	    if transient
	        form.addInflowCondition(inflowRegions[i], timeRamp*inflowFunction)
	    else:
	        form.addInflowCondition(inflowRegions[i], inflowFunction)
	    i += 1
	i = 0
    while i < numOutflows:
        form.addOutflowCondition(outflowRegions[i])
        i += 1
    i = 0
    while i < numWalls
        form.addWallCondition(region)
        i += 1
        
    form.solve()
    print("Solving...")
    #print("Solve completed in __ minutes, __ seconds")
    return form
