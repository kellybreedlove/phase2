from Singleton import *

@Singleton
class Reynolds:
	def __init__(self):
	    self.type = "Reynolds"
	def prompt(self):
		print("What Reynolds number?")
	def store(self, data):
	    if type(int(data)) == type(800):
	        self.Re = data
	        return True
	    else:
	        print(type(data))
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
	    return True
	def hasNext(self):
	    return True
	def next(self):
	    return MeshDimensions.Instance()
	    
@Singleton
class MeshDimensions:
	def __init__(self):
	     self.type = "MeshDimensions"
	def prompt(self):
		print('This solver handles rectangular meshes with lower-left corner at the origin./nWhat are the dimensions of your mesh? (E.g., "1.0 x 2.0")')
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
	    return True
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
	def store(self, data):
	    return True
	def hasNext(self):
	    return True
	def next(self):
	    return OutFlow.Instance()
	def undo(self):
	    return PolyOrder.Instance()
	    
@Singleton
class OutFlow:
	def __init__(self):
	     self.type = "OutFlow"
	def prompt(self):
		print("How many outflow conditions?")
	def store(self, data):
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
	def store(self, data):
	    return True
	def hasNext(self):
	    return False
	def undo(self):
	    return Outflow.Instance()
