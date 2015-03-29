from PyCamellia import *
from Plotter import *
import unittest


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
refinementNumber = 0
refCellVertexPoints = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]];



class TestPlotter(unittest.TestCase):
    
    """Test plotMesh"""
    def test_plotMesh(self):
        pass

    """ Test Plot"""
    def test_plot(self):
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        u1_soln = Function.solution(form.u(1),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

    
    """ Test Plot with p auto refine"""
    def test_plotPAutoRefine(self):   
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        form.pRefine()

        u1_soln = Function.solution(form.u(1),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

    """ Test Plot with h auto refine"""
    def test_plothAutoRefine(self):    
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        form.hRefine()

        u1_soln = Function.solution(form.u(1),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

    """ Test Plot with p manual refine"""
    def test_plotpManualRefine(self): 
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        activeCellIDs = mesh.getActiveCellIDs()
        #print activeCellIDs
        mesh.pRefine([3])

        u1_soln = Function.solution(form.u(1),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

    if __name__ == '__main__':
        unittest.main()
