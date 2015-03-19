from Singleton import *
from PyCamellia import *
import pickle # may not get used, we'll see

class SolverMemento(Object):
	def __init__(self, filename, soln, meshy):
		self.filename = filename
		self.soln = soln
		self.meshy = meshy
	def getSolution(self):
		pass
	def getMesh(self):
		pass
	def setSolution(self):
		pass
	def setMesh(self):
		pass

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
		pass
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
		self.prompts = ["What Reynolds number?", "Transient or steady state?", 'This solver handles rectangular meshes with lower-left corner at the origin./nWhat are the dimensions of your mesh? (E.g., "1.0 x 2.0")', 'How many elements in the initial mesh? (E.g. "3 x 5")',"What polynomial order? (1 to 9)", "How many inflow conditions?", "How many outflow conditions?","How many wall conditions?"]
		self.promptnum = 1
	def prompt(self):
		print(self.prompts[self.promptnum-1])
	def act(self, data):
		if data == "undo":
			if self.promptnum > 0:
				self.promptnum -= 1
				return self
			else:
				return InitState.Instance()
		else:
			if self.promptnum < len(self.prompts):
				self.promptnum += 1
				return self
			else:
				i = 1
				while i <= int(data):
					print("For wall condition " + str(i) + ', what region of space? (E.g. "x=0.5, y > 3")')
					i += 1

				self.promptnum = 1
				return PostSolveState.Instance()

@Singleton
class NavierStokesState:
	def __init__(self):
		self.prompts = ["What Reynolds number?", "Transient or steady state?", 'This solver handles rectangular meshes with lower-left corner at the origin./nWhat are the dimensions of your mesh? (E.g., "1.0 x 2.0")', 'How many elements in the initial mesh? (E.g. "3 x 5")',"What polynomial order? (1 to 9)", "How many inflow conditions?", "How many outflow conditions?","How many wall conditions?"]
		self.promptnum = 0
	def prompt(self):
		print(self.prompts[self.promptnum])
	def act(self, data):
		if data == "undo":
			if self.promptnum > 0:
				self.promptnum -= 1
				return self
			else:
				return InitState.Instance()
		else:
			if self.promptnum < len(self.prompts):
			    #save data or act appropriately
				self.promptnum += 1
				return self
			else:
				self.promptnum = 0
				return PostSolveState.Instance()

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
	self.filename
	def prompt(self):
		filename = input("What solution would you like to load?")
	def act(self, command):
	    	# load
		print ("Loading...")
		file = open(filename, 'rb') # open for reading
		memento = pickle.load(file) # may not use pickle, just a place holder
		file.close()
		Solver.setMemento(memento)
		print("loaded."

@Singleton
class SaveState:
	self.filename
	def prompt(self):
		filename = input("What would you like to call the solution and mesh files?")
	def act(self, command):
		# save file
		print ("Saving...")
		memento = Solver.createMemento()
		file = open(fileName, 'wb') # open for writing
		pickle.dump(memento, file) # may not use pickle, just a place holder
		file.close()
		print ("saved.")
	    	    
		return PostsolveState.Instance()

#run solver
if __name__ == '__main__':
	phase2 = Solver()
	# command = "input"
	phase2.state.prompt()
	command = str(input())
	while command != "exit":
		phase2.state = phase2.state.act(command)
		phase2.state.prompt()
		command = str(input())
