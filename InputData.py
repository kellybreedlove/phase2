from Singleton import *
from InflowParser import *
from ParseFunction import *
#import Solver

# The memento doesn't care about any of the data, it just passes it around
class Memento:
    def __init__(self, dataList):
        self.set(dataList)
    def get(self):
        return self.dataList
    def set(self, dataList):
        self.dataList = dataList

# should we restrict the creation of a memento to being only when the data is complete, and should we confirm it matches
# stokes vs nStokes requirements?
class InputData:
	def __init__(self, stokesOrNot):
		self.form = None #initialized to null value
		self.stokes = stokesOrNot #true if stokes, false if NavierStokes
		self.vars = [self.stokes] # to collect all the variables

                # NOT enough information to makes stokes form using SolutionFns, need polyOrder exc.

		# Stokes: stokesTrue, transient, dims [], numElements[], mesh, 
		#   polyOrder, inflow tuple (numInflows, [inflow regions], [x velocities], [y velocities]),
		#   outflow tuple (numOutflows, [outflow regions]), wall tuple (numWalls, [wall regions])
		# Navier Stokes: nStokesFalse, Reynolds, transient, dims[], numElements[], mesh, polyOrder, 
		#   inflow tuple, outflow tuple, wall tuple

	def setForm(self, form):
		self.form = form
	def getForm(self):
	    return self.form
	def addVariable(self, var):
		self.vars.append(var)
	def createMemento(self):
		return Memento([self.form, self.stokes] + self.vars) # shove it all into one list to hold onto
	def setMemento(self, memento):
		data = memento.get()
		self.form = data[0]	
		self.stokes = data[1]
		self.vars = data[2:]
		#if self.stokes:
                    #spaceDim = 2
                    #dims = self.vars[2]
                    #numElements = self.vars[3]
                    #polyOrder = self.vars[5]
                    #self.form = SolutionFns.steadyLinearInit(sapceDim, dims, numElements, polyOrder)
                    # initialize solution from here & use inflow and wall
                    # conditions to add to the initialized solution again
                    # can't say I understand if I should initialize a new form or use the stored one from memento

@Singleton
class Reynolds: #only used for Navier-Stokes
	def __init__(self):
	    self.type = "Reynolds"
	def prompt(self):
		print("What Reynolds number?")
	def store(self, inputData, datum):
	    try:
	        inputData.addVariable(int(datum))
	        return True
	    except ValueError:
	        return False
	def hasNext(self):
	    return True
	def next(self):
	    return State.Instance()

@Singleton
class State: #transient not supported for Navier-Stokes
	def __init__(self):
	    self.type = "State"
	def prompt(self):
		print("Transient or steady state?")
	def store(self, inputData, datum):
	    if datum.lower() == "transient" or datum.lower() == "steady state":
	        if inputData.stokes == false and datum.lower() == "transient"
	            print("Transient solves are not supported for Navier-Stokes")
	            return False
	        else:
	            inputData.addVariable(datum.lower())
	            return True
	    else:
	        return False
	def hasNext(self):
	    return True
	def next(self):
	    return MeshDimensions.Instance()
	def undo(self):
	    return Reynolds.Instance()
	    
@Singleton
class MeshDimensions:
	def __init__(self):
	     self.type = "MeshDimensions"
	def prompt(self):
		print('This solver handles rectangular meshes with lower-left corner at the origin.\nWhat are the dimensions of your mesh? (E.g., "1.0 x 2.0")')
	def store(self, inputData, datum):
		try:
		    dims = stringToDims(datum)
		    inputData.addVariable(dims)
		    return True
		except ValueError:
		    return False
	def hasNext(self):
		return True
	def next(self):
		return Elements.Instance()
	def undo(self):
		return State.Instance()
		
@Singleton
class Elements:
	def __init__(self):
	     self.type = "Elements"
	def prompt(self):
		print('How many elements in the initial mesh? (E.g. "3 x 5")')
	def store(self, inputData, datum): #enough info to create mesh
		try:
		    numElements = stringToElements(datum)
		    inputData.addVariable(numElements)
		    if inputData.vars[0]:
		        dims = inputData.vars[2]
		    else:
		        dims = inputData.vars[3]
		    x0 = [0.,0.]
		    #print(inputData.vars[0])
		    #print(inputData.vars[1])
		    #print(inputData.vars[2])
		    #print(dims)
		    meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
		    inputData.addVariable(meshTopo)
		    return True
		except ValueError:
		    return False
	def hasNext(self):
		return True
	def next(self):
		return PolyOrder.Instance()
	def undo(self):
		return MeshDimensions.Instance()
	    
@Singleton
class PolyOrder:
	def __init__(self):
	     self.type = "PolyOrder"
	def prompt(self):
		print("What polynomial order? (1 to 9)")
	def store(self, inputData, datum): #enough info to create NS form or initialize S solution
	    try:
	        order = int(datum)
	    	if order <= 9 and order >= 1:
			    inputData.addVariable(order)
			    if not inputData.stokes: #if NS
			        Re = inputData.vars[1]
			        meshTopo = inputData.vars[5]
			        inputData.form = NavierStokesVGPFormulation(meshTopo,Re,order,delta_k)
			    else: #if Stokes
			        meshTopo = inputData.vars[4]
			        inputData.form.initializeSolution(meshTopo,order,delta_k)
			    return True
	    	else:
			    return False
	    except ValueError:
	    	return False
	def hasNext(self):
	    return True
	def next(self):
	    return Inflow.Instance()
	def undo(self):
	    return Elements.Instance()
	    
@Singleton
class Inflow:
	def __init__(self):
	     self.type = "Inflow"
	def prompt(self):
		print("How many inflow conditions?")
	def store(self, inputData, datum): #returns True (proceed to Outflow), False (wrong input, try again), or "undo" (go bak to PolyOrder)
	    self.inflowRegions = []
	    self.inflowX = []
	    self.inflowY = []
	    try:
	        numInflows = int(datum)
	        i = 1
	        while i <= numInflows*3:
	        	x = self.obtainData(i)
	        	if not str(x) == "False":
	        	    i += 1
	        	    if str(x) == "undo":
	        	        i -= 2 #go back to last input
	        	    if i < 1:
	        	        return "undo"#already at last input, go back to PolyOrder
	        	else:
	        	    print("Sorry, input does not match expected format.")
	        inputData.addVariable((numInflows, self.inflowRegions, self.inflowX, self.inflowY))
	        i = 0
	        while i < numInflows:
	            inputData.form.addInflowCondition(self.inflowRegions[i], Function.vectorize(self.inflowX[i], self.inflowY[i])) #add inflow conditions
	            i += 1
	        return True
	    except ValueError:
	        return False
	def obtainData(self, i):#returns True (proceed to next input needed), False (wrong input, try again), or "undo" (go back to last input)
	    if (i+2)%3 == 0:
	        data = raw_input("For inflow condition " + str((i+2)/3) + ', what region of space? (E.g. "x=0.5, y > 3")\n')
	        if data.lower() == "undo":
	            return "undo"
	        elif data.lower() == "exit" or data.lower() == "quit":
	            quit()
	        else:
	            try:
	                region = stringToFilter(data.replace(" ", ""))
	                self.inflowRegions.append(region)
	                return True
	            except ValueError:
	                return False
	    elif (i+1)%3 == 0:
	        data = raw_input("For inflow condition " + str((i+1)/3) + ", what is the x component of the velocity?\n")
	        if data.lower() == "undo":
	            return "undo"
	        elif data.lower() == "exit" or data.lower() == "quit":
	            quit()
	        else:
	            try:
	                x = stringToFunction(data)
	                self.inflowX.append(x)
	                return True
	            except ValueError:
	                return False
	    elif i%3 == 0:
	        data = raw_input("For inflow condition " + str(i/3) + ", what is the y component of the velocity?\n")
	        if data.lower() == "undo":
	            return "undo"
	        elif data.lower() == "exit" or data.lower() == "quit":
	            quit()
	        else:
	            try:
	                y = stringToFunction(data)
	                self.inflowY.append(y)
	                return True
	            except ValueError:
	                return False
	    else:
	        return False
	def hasNext(self):
	    return True
	def next(self):
	    return Outflow.Instance()
	def undo(self):
	    return PolyOrder.Instance()
	    
@Singleton
class Outflow:
	def __init__(self):
	     self.type = "Outflow"
	def prompt(self):
		print("How many outflow conditions?")
	def store(self, inputData, datum): #returns True (proceed to Walls), False (wrong input, try again), or "undo" (go bak to Inflow)
	    self.outflowRegions = []
	    try:
	        numOutflows = int(datum)
	        i = 1
	        while i <= numOutflows:
	        	x = self.obtainData(i)
	        	if not str(x) == "False":
	        	    i += 1
	        	    if str(x) == "undo":
	        	        i -= 2 #go back to last input
	        	    if i < 1:
	        	        return "undo"#already at last input, go back to Inflow
	        	else:
	        	    print("Sorry, input does not match expected format.")
	        inputData.addVariable((numOutflows, self.outflowRegions))
	        i = 0
	        while i < numOutflows:
	            inputData.form.addOutflowCondition(self.outflowRegions[i])#add outflow conditions
	            i += 1
	        return True
	    except ValueError:
	        return False
	def obtainData(self, i):#returns True (proceed to next input needed), False (wrong input, try again), or "undo" (go back to last input)
	    data = raw_input("For outflow condition " + str(i) + ', what region of space? (E.g. "x=0.5, y > 3")\n')
	    if data.lower() == "undo":
	            return "undo"
	    elif data.lower() == "exit" or data.lower() == "quit":
	        quit()
	    else:
	        try:
	            region = stringToFilter(data.replace(" ", ""))
	            self.outflowRegions.append(region)
	            return True
	        except ValueError:
	            return False
	def hasNext(self):
	    return True
	def next(self):
	    return Walls.Instance()
	def undo(self):
	    return Inflow.Instance()
	    
@Singleton
class Walls:
	def __init__(self):
	     self.type = "Walls"
	def prompt(self):
		print("How many wall conditions?")
	def store(self, inputData, datum):#returns True (proceed), False (wrong input, try again), or "undo" (go bak to Outflow)
	    self.wallRegions =  []
	    try:
	        numWalls = int(datum)
	        i = 1
	        while i <= numWalls:
	        	x = self.obtainData(i,inputData)
	        	if not str(x) == "False":
	        	    i += 1
	        	    if str(x) == "undo":
	        	        i -= 2 #go back to last input
	        	    if i < 1:
	        	        return "undo"#already at last input, go back to Outflow
	        	else:
	        	    print("Sorry, input does not match expected format.")
	        inputData.addVariable((datum, self.wallRegions))
	        return True
	    except ValueError:
	        return False
	def obtainData(self, i, inputData):#returns True (proceed to next input needed), False (wrong input, try again), or "undo" (go back to last input)
	    data = raw_input("For wall condition " + str(i) + ', what region of space? (E.g. "x=0.5, y > 3")')
	    if data == "undo":
	        return "undo"
	    elif data.lower() == "exit" or data.lower() == "quit":
	        quit()
	    else:
	        try:
	            region = stringToFilter(data.replace(" ", ""))
	            inputData.form.addWallCondition(region)#add wall conditions
	            self.wallRegions.append(region)
	            return True
	        except ValueError:
	            return False
	def hasNext(self):
	    return False
	def undo(self):
	    return Outflow.Instance()
