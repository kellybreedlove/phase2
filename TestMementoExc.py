from PyCamellia import *
import pickle
import unittest
from SolutionFns import *

class TestLoadSave(unittest.TestCase):
    x0 = [0.,0.]
    spaceDim = 2
    dims = [1.0,1.0]
    numElements = [2,2]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
    delta_k = 1
    mu = 1.0
    useConformingTraces = True
    polyOrder = 3
    
    form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
    form.initializeSolution(meshTopo,polyOrder,delta_k)
    form.addZeroMeanPressureCondition()

    """Test Some Stuff"""
    def test_Stuff(self):
        pass

    if __name__ == '__main__':
        #unittest.main()
        filename = "steadyNavierStokes"
        
        try:
            exporter = HDF5Exporter(form.solution().mesh(), filename, ".")
            exporter.exportSolution(form.solution(),0)
            print "saved"
        except:
            print "save error"
        try:
            loadedSoln = Solution.loadFromHDF5("steadyNavierStokes/HDF5")
            print "loaded"
        except:
            print "load error"

        try:
            steadyNonlinearExport(form)
        except:
            print "save error"
        try:
            loadFromHDF5("steadyNavierStokes")
