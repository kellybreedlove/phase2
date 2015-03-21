from PyCamellia import *
import pickle

class StokesMemento:
    def __init__(self, form, dataTuple):
        self.form = form
        self.soln = form.solution()
        self.mesh = soln.mesh()
        self.reNum = dataTuple[1]
        self.transient = dataTuple[2]
        self.dims = dataTuple[3]
        self.numElements = dataTuple[4]
        self.polyOrder = dataTuple[5]
        self.inflow = dataTuple[6]
        self.outflow = dataTuple[7]
        self.wall = dataTuple[8]
        # handle inflow outflow and wall expansion
    def get(self):
        return ("stokes", self.form, self.soln, self.mesh, self.reNum, self.transient, self.dims, self.numElements, self.polyOrder, self.inflow, self.outflow, self.wall)
    def set(self, stokesTuple):
       (self.form, self.soln, self.mesh, self.reNum, self.transient, self.dims, self.numElements, self.polyOrder, self.inflow, self.outflow, self.wall) = stokesTuple
        #handle inflow outflow and wall expansion


class NavierStokesMemento:
    def __init__(self, form, dataTuple):
        self.form = form
        self.soln = form.solution()
        self.mesh = soln.mesh()
        self.transient = dataTuple[0]
        self.dims = dataTuple[1]
        self.numElements = dataTuple[2]
        self.polyOrder = dataTuple[3]
        self.inflow = dataTuple[4]
        self.outflow = dataTuple[5]
        self.wall = dataTuple[6]
        #handle inflow outflow and wall expansion
    def get(self):
        return ("nStokes", self.form, self.soln, self.mesh, self.transient, self.dims, self.numElements, self.polyOrder, self.inflow, self.outflow, self.wall)
    def set(self, nStokesTuple):
        (self.form, self.soln, self.mesh, self.transient, self.dims, self.numElements, self.polyOrder, self.inflow, self.outflow, self.wall) = nStokesTuple
        #handle inflow outflow and wall expansion
