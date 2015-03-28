from Singleton import *
from ConditionParser import *
from ParseFunction import *
from SolveFormulation import *
import re

# The memento doesn't care about any of the data, it just passes it around
class Memento:
    def __init__(self, dataMap):
        self.set(dataMap)
    def get(self):
        return self.dataMap
    def set(self, dataMap):
        self.dataMap = dataMap

class InputData:
    def __init__(self, stokesOrNot):
        self.vars = {"stokes": stokesOrNot} # to collect all the variables

        # Stokes: stokesTrue, transient, dims [], numElements[], mesh, 
        #   polyOrder, inflow tuple (numInflows, [inflow regions], [x velocities], [y velocities]),
        #   outflow tuple (numOutflows, [outflow regions]), wall tuple (numWalls, [wall regions])
        # Navier Stokes: nStokesFalse, Reynolds, transient, dims[], numElements[], mesh, polyOrder, 
        #   inflow tuple, outflow tuple, wall tuple

    def setForm(self, form):
        self.vars["form"] = form
    def getForm(self):
        try:
            return self.vars["form"]
        except:
            print("InputData does not contain form")
    def addVariable(self, string, var):
        self.vars[string] = var
    def getVariable(self, string):
        try: 
            return self.vars[string]
        except:
            print("InputData does not contain %s" % string)
    def createMemento(self):
        return Memento(self.vars)
    def setMemento(self, memento):
        self.vars = memento.get()

                    
@Singleton
class Reynolds: #only used for Navier-Stokes
	def __init__(self):
	    self.type = "Reynolds"
	def prompt(self):
            print("What Reynolds number?")
	def store(self, inputData, datum):
	    try:
                inputData.addVariable("reynolds",int(datum))
                return True
	    except ValueError:
	        print("Please enter an integer value.")
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
            try:
                datumL = datum.lower()
                if datumL == "transient" or datumL == "steady state":
                    if datumL == "steady state":
                        inputData.addVariable("transient", False) # steady state
                        return True
                    elif (not inputData.getVariable("stokes")) and datumL == "transient":
                        print("Transient solves are not supported for Navier-Stokes")
                        return False
                    else:
                        inputData.addVariable("transient", True)
                        return True
                else:
                    print('Please enter "transient" or "steady state"')
                    return False
            except AttributeError:
                print("Please enter a string value.")
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
		    dims = stringToDims(str(datum).strip())
		    inputData.addVariable("meshDimensions", dims)
		    return True
		except ValueError:
		    print('Please enter two floating point values separated by an "x", E.g., "1.0 x 2.0")')
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
		    numElements = stringToElements(str(datum).strip())
                    inputData.addVariable("numElements", numElements)
		    return True
		except ValueError:
		    print('Please enter two integer values separated by an "x", E.g., "3 x 5"')
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
			    inputData.addVariable("polyOrder",order)
			    return True
			else:
			    return False
		except ValueError:
			print("Please enter an integer value 1 to 9")
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
	    self.Regions = []
	    self.X = []
	    self.Y = []
	    if str(type(datum)) == int:
	        numOutflows = int(datum)
	    else:
	        print("Please enter an integer value")
	        return False
	    i = 1
	    while i <= numInflows*3:
	        x = self.obtainData(i)
	        if not str(x) == "False":
	            i += 1
	            if str(x) == "undo":
	                i -= 2 #go back to last input
	            if i < 1:
	                return "undo"#already at last input, go back to PolyOrder
	    inputData.addVariable("numInflows",numInflows)
	    inputData.addVariable("inflowRegions", self.Regions)
	    inputData.addVariable("inflowX", self.X)
	    inputData.addVariable("inflowY", self.Y)
	    return True
	def obtainData(self, i):#returns True (proceed to next input needed), False (wrong input, try again), or "undo" (go back to last input)
	    if (i+2)%3 == 0:
	        return getFilter(promptRegion(i, "inflow"),self.Regions)
	    elif (i+1)%3 == 0:
	        return getFunction(promptInflowFun((i+1)/3, "x"),self.X)
	    elif i%3 == 0:
	        return getFunction(promptInflowFun(i/3, "y"),self.Y)
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
	    if str(type(datum)) == int:
	        numOutflows = int(datum)
	    else:
	        print("Please enter an integer value")
	        return False
	    i = 1
	    while i <= numOutflows:
	        x = getFilter(promptRegion(i, "outflow"),self.Regions)#returns True (proceed to next input needed), False (wrong input, try again), or "undo" (go back to last input)
	        if not str(x) == "False":#either "True" or "undo"
	            i += 1
	            if str(x) == "undo":
	                i -= 2 #go back to last input
	            if i < 1:
	                return "undo"#already at last input, go back to Inflow
	    inputData.addVariable("numOutflows",numOutflows)
	    inputData.addVariable("outflowRegions", self.outflowRegions)
	    return True
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
	    if str(type(datum)) == int:
	        numOutflows = int(datum)
	    else:
	        print("Please enter an integer value")
	        return False
	    i = 1
	    while i <= numWalls:
	    	x = getFilter(promptRegion(i, "wall"), inputData.wallRegions)#returns True (proceed to next input needed), False (wrong input, try again), or "undo" (go back to last input)
	    	if not str(x) == "False":
	    	    i += 1
	    	    if str(x) == "undo":
	    	        i -= 2 #go back to last input
	    	    if i < 1:
	    	        return "undo"#already at last input, go back to Outflow
	    	else:
	    	    return False
	    inputData.addVariable("numWalls", datum)
	    inputData.addVariable("wallRegions", self.wallRegions)
	    inputData.setForm(solve(inputData.vars))
	    return True
	def hasNext(self):
	    return False
	def undo(self):
	    return Outflow.Instance()

"""
Some methods for retreiving data input
"""

   
def promptRegion(i, inoutwall):
    data = raw_input("For " + inoutwall + " condition " + str((i+2)/3) + ', what region of space? (E.g. "x=0.5, y > 3")\n')
    return data
    
def getFilter(data, flowRegions): #returns True, False, or undo
        if data.lower() == "undo":
            return "undo"
        elif data.lower() == "exit" or data.lower() == "quit":
            quit()
        else:
            try:
                region = stringToFilter(data.replace(" ", ""))
                flowRegions.append(region)
                return True
            except ValueError:
                print('Please enter the constraints on x, if any, followed by the restraints on y,\nif any, separated by a comma (E.g. "x=0.5, y > 3")')
                return False

def promptInflowFun(i,var):
    data = raw_input("For inflow condition " + str(i) + ", what is the " + str(var) + " component of the velocity?\n")
    return data

def getFunction(data, store):
    if data.lower() == "undo":
        return "undo"
    elif data.lower() == "exit" or data.lower() == "quit":
        quit()
    else:
        try:
            y = stringToFunction(data)
            store.append(y)
            return True
        except ValueError as e:
            print(e)
            return False


"""
Some methods for formatting data input
"""
def stringToDims(inputstr):
    try:
        tokenList = re.split('x', inputstr)
        x = float(tokenList[0])
        y = float(tokenList[1])
        print(x)
        print(y)
        return [x,y]
    except:
        raise ValueError

def stringToElements(inputstr):
    try:
        tokenList = re.split('x', inputstr)
        x = int(tokenList[0])
        y = int(tokenList[1])
        print(x)
        print(y)
        return [x,y]
    except:
        raise ValueError
