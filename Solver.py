from Singleton import *
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
		with open('stokesText') as f: self.prompts = f.readlines()
		f.close()
		self.reset()
	def reset(self):
		self.promptnum = 0
		self.datastr = [] #to store user input as strings 
		  #(state, dimensions, elements, polyorder)
		self.inflowRegions = []
		self.inflowX = []
		self.inflowY = []
		self.outflowRegions = []
		self.wallRegions = []
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
			if self.promptnum < 4 and self.promptnum <= len(self.datastr):
				self.datastr.append(data)
			elif self.promptnum < 4:
				self.datastr[self.promptnum] = data
			elif self.promptnum == 4:
				i = 1
				while i <= int(data):
					inflowcondition = raw_input("For inflow condition " + str(i) + ', what region of space? (E.g. "x=0.5, y > 3")')
					inflowX = raw_input("For inflow condition " + str(i) + ", what is the x component of the velocity?")
					inflowY = raw_input("For inflow condition " + str(i) + ", what is the y component of the velocity?")
					if i-1 <= len(self.inflowRegions):
						self.inflowRegions.append(inflowcondition)
						self.inflowX.append(inflowX)
						self.inflowY.append(inflowY)
					else:
						self.inflowRegions[i-1] = inflowcondition
						self.inflowX[i-1] = inflowX
						self.inflowY[i-1] = inflowY
					i += 1
			elif self.promptnum == 5:
				i = 1
				while i < int(data):
					outflowcondition = raw_input("For outflow condition " + str(i) + ', what region of space? (E.g. "x=0.5, y > 3")')
					if i-1 <= len(self.outflowRegions):
						self.inflowRegions.append(outflowcondition)
					else:
						self.outflowRegions[i-1] = outflowcondition
					i += 1
			else:
				i = 1
				while i <= int(data):
					self.wallRegions = raw_input("For wall condition " + str(i) + ', what region of space? (E.g. "x=0.5, y > 3")')
					i += 1

				self.promptnum = 1
				#test print
				print(str(self.datastr))
				self.reset()
				return PostSolveState.Instance()
			self.promptnum += 1
			return self

@Singleton
class NavierStokesState:
	def __init__(self):
		with open('navierStokesText') as f: self.prompts = f.readlines()
		f.close()
		self.promptnum = 0
		self.datastr = []
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
