from Singleton import *

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
	def setMemento(self,memento):
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
				self.promptnum += 1
				return self
			else:
				self.promptnum = 0
				return PostSolveState.Instance()

@Singleton
class PostSolveState:
	def prompt(self):
		print("You can now: plot, refine, save, load, or exit.")

@Singleton
class PlotState:
	pass

@Singleton
class RefineState:
	pass

@Singleton
class LoadState:
	def prompt(self):
		print("What solution would you like to load?")

@Singleton
class SaveState:

phase2 = Solver()
command = "input"
while command != "exit":
	phase2.state.prompt()
	command = input()
	phase2.state = phase2.state.act(command)
