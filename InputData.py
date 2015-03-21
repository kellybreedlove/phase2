from Singleton import *
from InflowParser import *

@Singleton
class Reynolds: #only used for Navier-Stokes
	def __init__(self):
	    self.type = "Reynolds"
	def prompt(self):
		print("What Reynolds number?")
	def store(self, data):
	    try:
	        self.Re = int(data)
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
	def store(self, data):
	    if data.lower() == "transient" or data.lower() == "steady state":
	        self.state = data.lower()
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
	def store(self, data):
	    return True
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
	def store(self, data):
	    return True
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
	def store(self, data):
	    try:
	        self.order = int(data)
	        if self.order <= 9 and self.order >= 1:
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
	def store(self, data): #returns True (proceed to Outflow), False (wrong input, try again), or "undo" (go bak to PolyOrder)
	    self.inflowRegions = []
	    self.inflowX = []
	    self.inflowY = []
	    try:
	        self.numInflows = int(data)
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
	            self.inflowRegions.append(data)
	            return True
	    elif (i+1)%3 == 0:
	        data = raw_input("For inflow condition " + str((i+1)/3) + ", what is the x component of the velocity?\n")
	        if data.lower() == "undo":
	            return "undo"
	        elif data.lower() == "exit" or data.lower() == "quit":
	            quit()
	        else:
	            self.inflowX.append(data)
	            return True
	    elif i%3 == 0:
	        data = raw_input("For inflow condition " + str(i/3) + ", what is the y component of the velocity?\n")
	        if data.lower() == "undo":
	            return "undo"
	        elif data.lower() == "exit" or data.lower() == "quit":
	            quit()
	        else:
	            self.inflowY.append(data)
	            return True
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
	def store(self, data): #returns True (proceed to Walls), False (wrong input, try again), or "undo" (go bak to Inflow)
	    self.outflowRegions = []
	    try:
	        self.numOutflows = int(data)
	        i = 1
	        while i <= self.numOutflows:
	        	x = self.obtainData(i)
	        	if not str(x) == "False":
	        	    i += 1
	        	    if str(x) == "undo":
	        	        i -= 2 #go back to last input
	        	    if i < 1:
	        	        return "undo"#already at last input, go back to Inflow
	        	else:
	        	    print("Sorry, input does not match expected format.")
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
	        self.outflowRegions.append(data)
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
	def store(self, data):#returns True (proceed), False (wrong input, try again), or "undo" (go bak to Outflow)
	    self.wallRegions =  []
	    try:
	        self.numWalls = int(data)
	        i = 1
	        while i <= self.numWalls:
	        	x = self.obtainData(i)
	        	if not str(x) == "False":
	        	    i += 1
	        	    if str(x) == "undo":
	        	        i -= 2 #go back to last input
	        	    if i < 1:
	        	        return "undo"#already at last input, go back to Outflow
	        	else:
	        	    print("Sorry, input does not match expected format.")
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
	        self.wallRegions.append(data)
	        return True
	def hasNext(self):
	    return False
	def undo(self):
	    return Outflow.Instance()
