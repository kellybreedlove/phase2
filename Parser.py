from PyCamellia import *
import pickle # may not get used, we'll see

class Memento(object):
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
