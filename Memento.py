from PyCamellia import *
import pickle

class SolutionMemento:
    def __init__(self, solution):
        self.soln = solution
        self.mesh = solution.mesh()
    def getSolution(self):
        pass
    def setSolution(self):














def createMemento(self):
    return SolutionMemento(self.soln)
