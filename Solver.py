from Singleton import *
from InputData import *
from RefineStates import *
from RefineP import *
import pickle
from Plotter import *
from itertools import chain, combinations

class Solver:
	def __init__(self):
		self.commands = []
		self.state = InitState.Instance()
		self.inputData = None # initally null until some input is known
		#self.state = StokesState.Instance() #FOR TESTING
	def readCommand(self, userinput):
		command = userinput.lower()
		if not command == "" and command[0] == " ":
		    self.readCommand(command[1:])
		else:
		    if " " in command and not command[:6] == "steady" and not "x" in command:
		    	self.readCommand(command[:command.index(" ")])
		    	self.readCommand(command[(command.index(" ")+1):])
		    else:
		    	#print(command) #for testing
		    	self.state = self.state.act(command, self)
	def prompt(self):
		self.state.prompt()

@Singleton
class InitState:
	def __init__(self):
		print("Welcome to the PyCamellia incompressible flow solver!")
	def prompt(self):
		print("You can now: create or load.")
	def act(self, command, context):
		if command.lower() == "create":
			print("Before we solve, I need to ask you some setup questions.")
			return CreateState.Instance()
		elif command.lower() == "load":
			return LoadState.Instance()
		elif command.lower() == "undo":
			print("Unable to undo.")
			return self
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
	def act(self, sns, context):
		if sns.lower() == "stokes" or sns.lower() == "s":
			context.inputData = InputData(True)
			return StokesState.Instance()
		elif sns.lower() == "navier-stokes" or sns.lower() == "ns":
			context.inputData = InputData(False)
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
	def act(self, datum, context):
		if datum.lower() == "undo":
			if self.inputState.type == "State":
				return CreateState.Instance()
			else:
				self.inputState = self.inputState.undo()
				return self
		else:
			x = self.inputState.store(context.inputData, datum)
			if not str(x) == "False":
				if self.inputState.hasNext():
					self.inputState = self.inputState.next()
					return self
				else:
					return PostSolveState.Instance()
			else:
				return self

@Singleton
class NavierStokesState:
	def __init__(self):
		self.inputState = Reynolds.Instance()
	def prompt(self):
		self.inputState.prompt()
	def act(self, datum, context):
		if datum.lower() == "undo":
			if self.inputState.type == "Reynolds":
				return CreateState.Instance()
			else:
				self.inputState = self.inputState.undo()
				return self
		else:
			x = self.inputState.store(context.inputData, datum)
			if not str(x) == "False":
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
	def act(self, command, context):
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
	def act(self, command, context):
		combos = combinations([-1.,1.,0.,.5,-.5,.25,-.25,.75,-.75,.8,-.8,.1,-.1,.2,-.2,.3,-.3,.4,-.4,.6,-.6,.7,-.7,.8,-.8,.9,-.9,.15,-.15,.35,-.35,.45,-.45,.55,-.55,.65,-.65,.85,-.85,.95,-.95,.125,-.125,.175,-.175,.225,-.225,.275,-.275,.325,-.325,.375,-.375,.425,-.425,.475,-.475,.525,-.525,.575,-.575,.625,-.625,.675,-.675,.725,-.725,.825,-.825,.875,-.875,.925,-.925,.975,-.975,.33,-.33,.66,-.66],2)
		refCellVertexPoints = []
		p = []
		v = []
		for e in combos:
			refCellVertexPoints.append(list(e))
		form = context.inputData.getForm()
		mesh = form.solution().mesh()
		activeCellIDs = mesh.getActiveCellIDs()
		perCellError = form.solution().energyErrorPerCell()
		if command.lower() == "u1":
			print("Plotting " + command + "...")
			u1_soln = Function.solution(form.u(1),form.solution())
			for cellID in activeCellIDs:
			    (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
			    p.append(points)
			    v.append(values)
			plot(v, p)
			
			#plot
		elif command.lower() == "u2":
			print("Plotting " + command + "...")
			u2_soln = Function.solution(form.u(2),form.solution())
			for cellID in activeCellIDs:
			    (values,points) = u2_soln.getCellValues(mesh,cellID,refCellVertexPoints)
			    p.append(points)
			    v.append(values)
			plot(v, p)
			#plot
		elif command.lower() == "p":
			print("Plotting " + command + "...")
			p_soln = Function.solution(form.p(),form.solution())
			for cellID in activeCellIDs:
			    (values,points) = p_soln.getCellValues(mesh,cellID,refCellVertexPoints)
			    p.append(points)
			    v.append(values)
			plot(v, p)
			#plot
		elif command.lower() == "stream function":
			print("Solving for stream function...")
			stream_soln = Function.solution(form.streamPhi(), form.solution())
			for cellID in activeCellIDs:
			    (values,points) = stream_soln.getCellValues(mesh,cellID,refCellVertexPoints)
			    p.append(points)
			    v.append(values)
			plot(v, p)
				
			#solve
			print("Plotting " + command + "...")
			#refine
		elif command.lower() == "mesh":
			print("Plotting " + command + "...")
			plotMesh(activeCellIDs,mesh,"Mesh")
			#refine
		elif command.lower() == "error":
			print("Plotting " + command + "...")
			plotError(activeCellIDs,perCellError,mesh,"Error")
			#refine
		else:
			print("Sorry, input does not match any known commands.")
			print("Please select  u1, u2, p, stream function, mesh, or error.")
			return self

@Singleton
class RefineState:
	def prompt(self):
		print("What sort of refinement would you like to make? (h or p)")
	def act(self, command, context):
		if command.lower() == "undo":
		    return PostSolveState.Instance()
		elif command.lower() == "h":
		    return hRefine.Instance()
		elif command.lower() == "p":
		    return pRefine.Instance()
		else:
			print("Sorry, input does not match any known commands.")
			print("Please select h or p to refine.")
			return self

@Singleton
class LoadState:
	def prompt(self):
		print("What solution would you like to load?")
	def act(self, command, context):
		if command == "undo":
		    return PostSolveState.Instance()
		else:
			try:
			    print("Loading..."),
		
			    file = open(command)
			    memento = pickle.load(file)
			    file.close()
			    context.inputData.setMemento(memento)
			
			    form = None
			    polyOrder = context.inputData.getVariable("polyOrder")
			    if not context.inputData.getVariable("stokes"):
			        spaceDim = 2
			        reynolds = context.inputData.getVariable("reynolds")
			        form = NavierStokesVGPForumlation(command + "Form", spaceDim, reynolds, polyOrder)
			    else:
			        form.initializeSolution(command + "Form", polyOrder)
			    
			    context.inputData.setForm(form)
			
			    mesh = form.solution().mesh()
			    elementCount = mesh.numActiveElements()
			    globalDofCount = mesh.numGlobalDofs()
			    print ("...loaded. Mesh has %s elements and %s degrees of freedom" % (elementCount, globalDofCount))
			    return PostSolveState.Instance()
			except (OSError, IOError):
			    print("No solution was found with the name \"%s\"" % command)
			    return LoadState.Instance()


@Singleton
class SaveState:
	def prompt(self):
		print("What would you like to call the solution and mesh files?")
	def act(self, command, context):
		if command == "undo":
		    return PostsolveState.Instance()
		else:
		    print("Saving..."),
		    form = context.inputData.getForm()
		    form.save(command + "Form")
		    memento = context.inputData.createMemento()
		    saveFile = open(command, 'wb')
		    pickle.dump(memento, saveFile)
		    saveFile.close()
		
		    print("saved.")
		    return PostsolveState.Instance()

#run solver
if __name__ == '__main__':
	phase2 = Solver()
	# command = "input"
	phase2.prompt()
	command = raw_input()
	while str(command).lower() != "exit" and str(command).lower() != "quit":
		phase2.readCommand(command.lower())
		phase2.prompt()
		command = raw_input()
