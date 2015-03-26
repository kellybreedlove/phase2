from Singleton import *
from InflowParser import *
from ParseFunction import *
import Solver

# The memento doesn't care about any of the data, it just passes it around
class Memento:
    def __init__(self, dataTuple):
        self.set(dataTuple)
    def get(self):
        return self.dataTuple
    def set(self, dataTuple):
        self.dataTuple = dataTuple

class InputData:
	def __init__(self, stokesOrNot):
		self.form = None #initialized to null value
		self.stokes = stokesOrNot #true if stokes, false if NavierStokes
		self.vars = () # to collect all the variables

		# Stokes: stokesTrue, reNum, transient, dims, numElements, 
		#   polyOrder, inflow tuple (numInflows, [inflow regions], [x velocities], [y velocities]),
		#   outflow tuple (numOutflows, [outflow regions]), wall tuple (numWalls, [wall regions])
		# Navier Stokes: nStokesFalse, transient, dims, numElements, polyOrder, 
		#   inflow tuple, outflow tuple, wall tuple

	def setForm(self, form,):
		self.form = form
	def addVariable(self, var):
		self.vars += (var,)
	def createMemento(self):
		return Memento((self.form, self.stokes) + self.vars) # shove it all into one tuple to hold onto
	def setMemento(self, memento):
		data = memento.get()
		self.form = data[0]	
		self.stokes = data[1]
		self.vars = data[2:]
		if stokes:
			polyOrder = self.vars[5]
		#self.form.initializeSolution(meshTopo,polyOrder, delta_k)
		# initialize solution from here & use inflow and wall
		# conditions to add to the initialized solution again

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
class State:
	def __init__(self):
	    self.type = "State"
	def prompt(self):
		print("Transient or steady state?")
	def store(self, inputData, datum):
	    if datum.lower() == "transient" or datum.lower() == "steady state":
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
		    #check data, create mesh
		    inputData.addVariable(datum)
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
	def store(self, inputData, datum):
		try:
		    #check data
		    inputData.addVariable(datum)
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
	def store(self, inputData, datum):
	    try:
	        order = int(datum)
	    	if order <= 9 and order >= 1:
			    inputData.addVariable(order)
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
	        self.numInflows = int(datum)
	        i = 1
	        while i <= self.numInflows*3:
	        	x = self.obtainData(i)
	        	if not str(x) == "False":
	        	    i += 1
	        	    if str(x) == "undo":
	        	        i -= 2 #go back to last input
	        	    if i < 1:
	        	        return "undo"#already at last input, go back to PolyOrder
	        	else:
	        	    print("Sorry, input does not match expected format.")
	        inputData.addVariable((datum, self.inflowRegions, self.inflowX, self.inflowY))
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
	                #parse data, create spatialFilter
	                self.inflowRegions.append(data)
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
	        inputData.addVariable((datum, self.outflowRegions))
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
	            #parse data, make spatialFilter
	            self.outflowRegions.append(data)
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
	        	x = self.obtainData(i)
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
	def obtainData(self, i):#returns True (proceed to next input needed), False (wrong input, try again), or "undo" (go back to last input)
	    data = raw_input("For wall condition " + str(i) + ', what region of space? (E.g. "x=0.5, y > 3")')
	    if data == "undo":
	        return "undo"
	    elif data.lower() == "exit" or data.lower() == "quit":
	        quit()
	    else:
	        try:
	            #parse data, create SpatialFilter
	            self.wallRegions.append(data)
	            return True
	        except ValueError:
	            return False
	def hasNext(self):
	    return False
	def undo(self):
	    return Outflow.Instance()
