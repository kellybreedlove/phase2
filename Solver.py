from Singleton import *
from InputData import *
#from PyCamellia import *

class Solver:
	def __init__(self):
		self.commands = []
		self.state = InitState.Instance()
		self.inputData = None # initally null until some input is known
		#self.state = StokesState.Instance() #FOR TESTING
	def readCommand(self, command):
		if " " in command:
			self.readCommand(self, command[command.index(" "):])
		else:
			self.state.act(command)

@Singleton
class InitState:
	def __init__(self):
		print("Welcome to the PyCamellia incompressible flow solver!")
	def prompt(self):
		print("You can now: create or load.")
	def act(self, command):
		if command.lower() == "create":
			print("Before we solve, I need to ask you some setup questions.")
			return CreateState.Instance()
		elif command.lower() == "load":
			return LoadState.Instance()
		elif command.lower() == "exit" or command.lower() == "quit":
			quit()
		else:
			print("Sorry, input does not match any known commands.")
			return self

@Singleton
class CreateState:
	def __init__(self):
		pass
	def prompt(self):
		print("Would you like to solve Stokes or Navier-Stokes?")
	def act(self, sns):
		if sns.lower() == "stokes" or sns.lower() == "s":
			inputData = InputData(True)
			return StokesState.Instance()
		elif sns.lower() == "navier-stokes" or sns.lower() == "ns":
			inputData = InputData(False)
			return NavierStokesState.Instance()
		elif sns.lower() == "undo":
			return InitState.Instance()
		else:
			print("Sorry, input does not match any known commands.")
			return self

@Singleton
class StokesState:
	def __init__(self):
		self.inputState = State.Instance()
	def prompt(self):
		self.inputState.prompt()
	def act(self, data):
		if data.lower() == "undo":
			if self.inputState.type == "State":
				return CreateState.Instance()
			else:
				self.inputState = self.inputState.undo()
				return self
		else:
			x = self.inputState.store(inputData, data)
			if not str(x) == "False":
				if str(x).lower() == "undo":
					self.inputState = self.inputState.undo()
					return self
				elif str(x).lower() == "exit" or str(x).lower() == "quit":
					quit()
				elif self.inputState.hasNext():
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
		self.inputState = Reynolds.Instance()
	def prompt(self):
		self.inputState.prompt()
	def act(self, data):
		if data.lower() == "undo":
			if self.inputState.type == "Reynolds":
				return CreateState.Instance()
			else:
				self.inputState = self.inputState.undo()
				return self
		else:
			x = self.inputState.store(inputData, data)
			if not str(x) == "False":
				if str(x).lower() == "undo":
					self.inputState = self.inputState.undo()
					return self
				elif str(x).lower() == "exit" or str(x).lower() == "quit":
					quit()
				elif self.inputState.hasNext():
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
		if command.lower() == "plot":
			return PlotState.Instance()
		elif command.lower() == "refine":
			return RefineState.Instance()
		elif command.lower() == "save":
			return SaveState.Instance()
		elif command.lower() == "load":
			return LoadState.Instance()
		elif command.lower() == "exit" or command.lower() == "quit":
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
		if command.lower() == "u1":
			print("Ploting " + command + "...")
			#plot
		elif command.lower() == "u2":
			print("Ploting " + command + "...")
			#plot
		elif command.lower() == "p":
			print("Ploting " + command + "...")
			#plot
		elif command.lower() == "stream function":
			print("Solving for stream function...")
			#solve
			print("Ploting " + command + "...")
			#refine
		elif command.lower() == "mesh":
			print("Ploting " + command + "...")
			#refine
		elif command.lower() == "error":
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
		if command.lower() == "h auto":
			print("Automatically refining in h . . .")
			#refine
			#print "New mesh has __ elements and __ degrees of freedom"
			#solve
			#print "Solve completed in _ minutes
			return PostSolveState.Instance()
		elif command.lower() == "h manual":
			#refine
			return PostSolveState.Instance()
		elif command.lower() == "p auto":
			print("Automatically refining in p . . .")
			#refine
			#print "New mesh has __ elements and __ degrees of freedom"
			#solve
			#print "Solve completed in _ minutes 
			return PostSolveState.Instance()
		elif command.lower() == "p manual":
			#refine
			return PostSolveState.Instance()
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
		file = open(self.filename) # open for reading
		memento = pickle.load(file) # may not use pickle, just a place holder
		file.close()
		inputData.setMemento(memento)
		#print ("...loaded. Mesh has %s elements and %s degrees of freedom" % (numEL, numDeg))
		return PostSolveState.Instance()


@Singleton
class SaveState:
	def prompt(self):
		print("What would you like to call the solution and mesh files?")
	def act(self, command):
		# save file
		print "Saving..."
		memento = inputData.createMemento()
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
	while str(command).lower() != "exit" and str(command).lower() != "quit":
		phase2.state = phase2.state.act(command)
		phase2.state.prompt()
		command = raw_input()
