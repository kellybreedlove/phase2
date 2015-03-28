from Singleton import *
from Solver import *
from SolutionFns import *

@Singleton
class hRefine:
    def prompt(self):
       print("Which elements? You can specify active element numbers (0,1,2,5,8,9,10,...) or auto.")
    def act(self, command, context):
        if command == "undo":
            return RefineState.Instance()
        elif command == "auto":
            form = context.inputData.getForm()
            print("Automatically refining in h . . .")
            if context.inputData.getVariable("stokes"): #stokes is linear
                form = steadyLinearHAutoRefine(form)
            else: #Navier-Stokes is nonlinear
                maxSteps = 20
                form = nonlinearHAutoRefine(form, maxSteps)
            mesh = form.solution().mesh()
            numActiveElements = mesh.numActiveElements()
            dof = mesh.numGlobalDofs()
            print("New mesh has " + str(numActiveelements) + " elements and " + str(dof) + " degrees of freedom.")
            #print("Solve completed in _ minutes")
        else:
            try:
                elements = parseElements(command)
                form = context.inputData.getForm()
                if context.inputData.getVariable("stokes"): #stokes is linear
                    form = linearHManualRefine(form, elements)
                else: #Navier-Stokes is nonlinear
                    form = nonlinearHManualRefine(form, elements)
                return PostSolveState.Instance()
            except ValueError:
            	print('Please enter integer values, separated by commas to indicate active elements, or "auto".')
            	return self

@Singleton
class pRefine:
    def prompt(self):
        print("Which elements? You can specify active element numbers (0,1,2,5,8,9,10,...) or auto.")
    def act(self, command, context):
        if command == "undo":
            return RefineState.Instance()
        elif command == "auto":
            form = context.inputData.getForm()
            print("Automatically refining in p . . .")
            if context.inputData.getVariable("stokes"): #stokes is linear
                form = steadyLinearPAutoRefine(form)
            else: #Navier-Stokes is nonlinear
                maxSteps = 20
                form = nonlinearPAutoRefine(form, maxSteps)
            mesh = form.solution().mesh()
            numActiveElements = mesh.numActiveElements()
            dof = mesh.numGlobalDofs()
            print("New mesh has " + str(numActiveelements) + " elements and " + str(dof) + " degrees of freedom.")
        else:
            try:
                elements = parseElements(command)
                form = context.inputData.getForm()
                if context.inputData.getVariable("stokes"): #stokes is linear
                    form = linearPManualRefine(form, elements)
                else:
                    form = linearPManualRefine(form, elements)
                return PostSolveState.Instance()
            except ValueError:
                print('Please enter integer values, separated by commas to indicate active elements, or "auto".')
                return self
    
def parseElements(elements):
    elementList = []
    while "," in elements:
        comma = elements.index(",")
        elementList.append(int(elements[:comma]))
        elements = elements[comma:]
    return elements
