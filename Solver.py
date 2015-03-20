from Singleton import *
from InputData import *
#from PyCamellia import *
import pickle # may not get used, we'll see

class SolverMemento:
	def __init__(self, form):
		self.form = form
		#self.soln = soln
		#self.meshy = meshy
	def getSolution(self):
		pass
#return self.soln
	def getMesh(self):
		pass
		#return self.meshy
	def setSolution(self, soln):
		pass
		#self.soln = soln
	def setMesh(self, meshy):
		pass
		#self.meshy = meshy

class Solver:
	def __init__(self):
		self.commands = []
		self.state = InitState.Instance()
	def readCommand(self, command):
		if " " in command:
			self.readCommand(self, command[command.index(" "):])
		else:
			self.state.act(command)
	def createMemento(self):
		return SolverMemento(self.form) # find soln, meshy
	def setMemento(self, memento):
		pass

@Singleton
class InitState:
	def __init__(self):
		print("Welcome to the PyCamellia incompressible flow solver!")
	def prompt(self):
		print("You can now: create or load.")
	def act(self, command):
		if command == "create":
			print("Before we solve, I need to ask you some setup questions.")
			return CreateState.Instance()
		elif command == "load":
			return LoadState.Instance()
		elif command == "exit" or command == "quit":
			return self
		else:
			print("Sorry, input does not match any known commands.")
			return self

@Singleton
class CreateState:
	def __init__(self):
		pass
	def prompt(self):
		print("Would you like to solve Stokes or Navier-Stokes?")
	def act(self, type):
		if type == "Stokes":
			return StokesState.Instance()
		elif type == "Navier-Stokes":
			return NavierStokesState.Instance()
		elif type == "undo":
			return InitState.Instance()
		else:
			print("Sorry, input does not match any known commands.")
			return self

@Singleton
class StokesState:
	def __init__(self):
		self.inputState = Reynolds.Instance()
	def prompt(self):
		self.inputState.prompt()
	def act(self, data):
		if data == "undo":
			if type(self.inputState) is Reynolds:
				return InitState.Instance()
			else:
				self.inputState = self.inputState.undo()
				return self
		else:
			if self.inputState.store(data):
				if self.inputState.hasNext():
					self.inputState = self.inputState.next()
					return self
				else:
					return PostSolveState.Instance()
			else:
				print("Sorry, input does not match expected format.")
				return self

@Singleton
class NavierStokesState:
	def __init__(self):
		self.inputState = State.Instance()
	def prompt(self):
		inputState.prompt()
	def act(self, data):
		if data == "undo":
			if type(self.inputState) is State:
				return InitState.Instance()
			else:
				self.inputState = self.inputState.undo()
				return self
		else:
			if self.inputState.act(data):
				if self.inputState.hasNext():
					self.inputState = self.inputState.next()
					return self
				else:
					return PostSolveState.Instance()
			else:
				print("Sorry, input does not match expected format.")
				return self


@Singleton
class PostSolveState:
	def prompt(self):
		print("You can now: plot, refine, save, load, or exit.")
	def act(self, command):
		if command == "plot":
			return PlotState.Instance()
		elif command == "refine":
			return RefineState.Instance()
		elif command == "save":
			return SaveState.Instance()
		elif command == "load":
			return LoadState.Instance()
		elif command == "exit" or command == "quit":
			return self
		else:
			print("Sorry, input does not match any known commands.")
			return self

@Singleton
class PlotState:
	def prompt(self):
		print("What would you like to plot?")
		print("Possible choices are: u1, u2, p, stream function, mesh, and error.")
	def act(self, command):
		if command == "u1":
			print("Ploting " + command + "...")
			#plot
		elif command == "u2":
			print("Ploting " + command + "...")
			#plot
		elif command == "p":
			print("Ploting " + command + "...")
			#plot
		elif command == "stream function":
			print("Solving for stream function...")
			#solve
			print("Ploting " + command + "...")
			#refine
		elif command == "mesh":
			print("Ploting " + command + "...")
			#refine
		elif command == "error":
			print("Ploting " + command + "...")
			#refine
		else:
			print("Sorry, input does not match any known commands.")
			print("Please select h or p auto or manual.")
			return self

@Singleton
class RefineState:
	def prompt(self):
		print("What would you like to refine?")
	def act(self, command):
		if command == "h auto":
			print("Automatically refining in h . . .")
			#refine
			#print "New mesh has __ elements and __ degrees of freedom"
			#solve
			#print "Solve completed in _ minutes 
		elif command == "h manual":
			#refine
			pass
		elif command == "p auto":
			print("Automatically refining in p . . .")
			#refine
			#print "New mesh has __ elements and __ degrees of freedom"
			#solve
			#print "Solve completed in _ minutes 
		elif command == "p manual":
			#refine
			pass
		else:
			print("Sorry, input does not match any known commands.")
			print("Please select h or p auto or manual.")
			return self

@Singleton
class LoadState:
	def prompt(self):
		self.filename = input("What solution would you like to load?")
	def act(self, command):
		# load
		file = open(filename) # open for reading
		memento = pickle.load(file) # may not use pickle, just a place holder
		file.close()
		Solver.setMemento(memento)
		#print ("...loaded. Mesh has %s elements and %s degrees of freedom" % (numEL, numDeg))
		return PostsolveState.Instance()


@Singleton
class SaveState:
	def prompt(self):
		print("What would you like to call the solution and mesh files?")
	def act(self, command):
		# save file
		print "Saving..."
		memento = Solver.createMemento()
		file = open(command, 'wb') # open for writing
		pickle.dump(memento, file) # may not use pickle, just a place holder
		file.close()
		print "saved."
		
		return PostsolveState.Instance()

#run solver
if __name__ == '__main__':
	phase2 = Solver()
	# command = "input"
	phase2.state.prompt()
	command = raw_input()
	while str(command) != "exit":
		phase2.state = phase2.state.act(command)
		phase2.state.prompt()
		command = raw_input()
