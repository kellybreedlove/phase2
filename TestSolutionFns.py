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
threshold = .05

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
    def test_steadyLinearInit(self):
        form = steadyLinearInit(dims, numElements, polyOrder)
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
        self.assertAlmostEqual(4, fooElementCount, elementCount)
        self.assertEqual(634, fooGlobalDofCount, globalDofCount)
        self.assertEqual(0.000, fooEnergyError, energyError)

        
    """Test addWall"""
    def test_addWall(self):
        form = steadyLinearInit(dims, numElements, polyOrder)
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
        form = steadyLinearInit(dims, numElements, polyOrder)
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


    """Test addOutflow"""
    def test_addOutflow(self):
        pass


    """Test energyPerCell"""
    def test_energyPerCell(self):
        form = steadyLinearInit(dims, numElements, polyOrder)
        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        foo.initializeSolution(meshTopo,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()

        addWall(form, notTopBoundary)
        addInflow(form, topBoundary, topVelocity)
        form.solve()

        perCellError = energyPerCell(form)
        
        foo.addWallCondition(notTopBoundary)
        foo.addInflowCondition(topBoundary,topVelocity)
        foo.solve()

        fooPerCellError = foo.solution().energyErrorPerCell()
        
        for cellID in fooPerCellError:
            if fooPerCellError[cellID] > .01:
                self.assertAlmostEqual(perCellError[cellID], fooPerCellError[cellID])


    """Test steadyLinearSolve"""
    def test_steadyLinearSolve(self):
        form = steadyLinearInit(dims, numElements, polyOrder)
        addWall(form, notTopBoundary)
        addInflow(form, topBoundary, topVelocity)
        steadyLinearSolve(form)

        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        foo.initializeSolution(meshTopo,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()
        foo.addWallCondition(notTopBoundary)
        foo.addInflowCondition(topBoundary,topVelocity)
        foo.solve()
        
        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()

        self.assertAlmostEqual(4, fooElementCount, elementCount)
        self.assertEqual(634, fooGlobalDofCount, globalDofCount)
        self.assertAlmostEqual(fooEnergyError, energyError)
        self.assertAlmostEqual(0.745, energyError, 3)


    """Test steadyLinearHAutoRefine"""
    def test_steadyLinearHAutoRefine(self):
        form = steadyLinearInit(dims, numElements, polyOrder)
        addWall(form, notTopBoundary)
        addInflow(form, topBoundary, topVelocity)
        steadyLinearSolve(form)

        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        mesh = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        foo.initializeSolution(mesh,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()
        foo.addWallCondition(notTopBoundary)
        foo.addInflowCondition(topBoundary,topVelocity)
        foo.solve()
        
        steadyLinearHAutoRefine(form)
        foo.hRefine()
        foo.solve()

        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()   
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()
        
        self.assertEqual(10, fooElementCount, elementCount)
        self.assertEqual(1502, fooGlobalDofCount, globalDofCount)
        self.assertAlmostEqual(fooEnergyError, energyError)
        self.assertAlmostEqual(0.660, energyError, 3)


    """Test steadyLinearPAutoRefine"""
    def test_steadyLinearPAutoRefine(self):
        form = steadyLinearInit(dims, numElements, polyOrder)
        addWall(form, notTopBoundary)
        addInflow(form, topBoundary, topVelocity)
        steadyLinearSolve(form)

        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshT = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        foo.initializeSolution(meshT,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()
        foo.addWallCondition(notTopBoundary)
        foo.addInflowCondition(topBoundary,topVelocity)
        foo.solve()
        
        steadyLinearPAutoRefine(form)
        foo.pRefine()
        foo.solve()

        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()   
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()
        
        self.assertEqual(4, fooElementCount, elementCount)
        self.assertEqual(780, fooGlobalDofCount, globalDofCount)
        self.assertAlmostEqual(fooEnergyError, energyError)
        self.assertAlmostEqual(0.700, energyError, 3)


    """Test steadyLinearHManualRefine"""
    def test_steadyLinearHManualRefine(self):
        form = steadyLinearInit(dims, numElements, polyOrder)
        addWall(form, notTopBoundary)
        addInflow(form, topBoundary, topVelocity)
        steadyLinearSolve(form)

        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshT = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        foo.initializeSolution(meshT,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()
        foo.addWallCondition(notTopBoundary)
        foo.addInflowCondition(topBoundary,topVelocity)
        foo.solve()

        mesh = form.solution().mesh()
        fooMesh = foo.solution().mesh()
        cellIDs = mesh.getActiveCellIDs()
        fooCellIDs = fooMesh.getActiveCellIDs()

        linearHManualRefine(form, cellIDs)
        fooMesh.hRefine(fooCellIDs)
        foo.solve()

        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()   
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()
        
        self.assertEqual(16, fooElementCount, elementCount)
        self.assertEqual(2402, fooGlobalDofCount, globalDofCount)
        self.assertAlmostEqual(fooEnergyError, energyError)
        self.assertAlmostEqual(0.660, energyError, 3)


    """Test steadyLinearPManualRefine"""
    def test_steadyLinearPManualRefine(self):
        form = steadyLinearInit(dims, numElements, polyOrder)
        addWall(form, notTopBoundary)
        addInflow(form, topBoundary, topVelocity)
        steadyLinearSolve(form)

        foo = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshT = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        foo.initializeSolution(meshT,polyOrder,delta_k)
        foo.addZeroMeanPressureCondition()
        foo.addWallCondition(notTopBoundary)
        foo.addInflowCondition(topBoundary,topVelocity)
        foo.solve()

        mesh = form.solution().mesh()
        fooMesh = foo.solution().mesh()
        cellIDs = mesh.getActiveCellIDs()
        fooCellIDs = fooMesh.getActiveCellIDs()

        linearPManualRefine(form, cellIDs)
        fooMesh.pRefine(fooCellIDs)
        foo.solve()

        mesh = form.solution().mesh()
        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        
        fooMesh = foo.solution().mesh()
        fooEnergyError = foo.solution().energyErrorTotal()   
        fooElementCount = fooMesh.numActiveElements()
        fooGlobalDofCount = fooMesh.numGlobalDofs()
        
        self.assertEqual(4, fooElementCount, elementCount)
        self.assertEqual(934, fooGlobalDofCount, globalDofCount)
        self.assertAlmostEqual(fooEnergyError, energyError)
        self.assertAlmostEqual(0.700, energyError, 3)


    """Test transientLinearInit"""
    def test_transientLinearInit(self):
        pass


    """Test transientLinearSolve"""
    def test_transientLienarSolve(self):
        pass


    """Test transientLinearRefine"""
    def test_transientLinearRefine(self):
        pass


    """Test transientLienarHRefine"""
    def test_transientLinearHRefine(self):
        pass


    """Test transientLinearPRefine"""
    def test_transientLinearPRefine(self):
        pass


    """Test steadyNonlinearInit"""
    def test_steadyNonlinearInit(self):
        pass

    """Test nonlinearSolve"""
    def test_nonlinearSolve(self):
        pass


    """Test steadyNonlinearSolve"""
    def test_steadyNonlinearSolve(self):
        pass


    """Test steadyNonlinearRefine"""
    def test_steadyNonlinearRefine(self):
        pass


    """Test steadyNonlinearHRefine"""
    def test_steadyNonlinearHRefine(self):
        pass


    """Test steadyNonlinearPRefine"""
    def test_steadyNonlinearPRefine(self):
        pass


    if __name__ == '__main__':
        unittest.main()
