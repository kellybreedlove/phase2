from PyCamellia import *
from SolutionFns import *
import unittest

"""
A whole bunch of variable so that the tests are not cluttered
"""
spaceDim = 2
useConformingTraces = True
mu = 1.0
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
polyOrder = 3
delta_k = 1

topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)

class TestSolutionFns(unittest.TestCase):

    """Test Some Stuff"""
    def test_Stuff(self):
        pass

    """Test steadyLinearInit"""
    def test_steadyLindearInit(self):
        form = steadyLinearInit(spaceDim, dims, numElements, polyOrder)
        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        foo.initializeSolution(meshTopo,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()
        
        form.solve()
        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        
        foo.solve()
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()
        
        self.assertIsNotNone(form)
        self.assertEqual(4, fooElementCount, elementCount)
        self.assertEqual(634, fooGlobalDofCount, globalDofCount)
        self.assertEqual(0.000, fooEnergyError, energyError)

        
    """Test addWall"""
    def test_addWall(self):
        form = steadyLinearInit(spaceDim, dims, numElements, polyOrder)
        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        foo.initializeSolution(meshTopo,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()

        foo.addWallCondition(notTopBoundary)
        addWall(form, notTopBoundary)

        form.solve()
        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        foo.solve()
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()

        self.assertEqual(4, fooElementCount, elementCount)
        self.assertEqual(634, fooGlobalDofCount, globalDofCount)
        self.assertEqual(0.000, fooEnergyError, energyError)


    """Test addInflowCondition"""
    def test_addInflowCondition(self):
        form = steadyLinearInit(spaceDim, dims, numElements, polyOrder)
        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        foo.initializeSolution(meshTopo,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()

        foo.addInflowCondition(topBoundary,topVelocity)
        addInflow(form, topBoundary, topVelocity)
        
        form.solve()
        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        foo.solve()
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()

        self.assertEqual(4, fooElementCount, elementCount)
        self.assertEqual(634, fooGlobalDofCount, globalDofCount)
        self.assertAlmostEqual(fooEnergyError, energyError)
        self.assertAlmostEqual(0.293, energyError, 3)

        foo.addWallCondition(notTopBoundary)
        addWall(form, notTopBoundary)

        form.solve()
        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        foo.solve()
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()

        self.assertEqual(4, fooElementCount, elementCount)
        self.assertEqual(634, fooGlobalDofCount, globalDofCount)
        self.assertAlmostEqual(fooEnergyError, energyError)
        self.assertAlmostEqual(0.745, energyError, 3)


    if __name__ == '__main__':
        unittest.main()
