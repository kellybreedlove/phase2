from PyCamellia import *
from Plotter import *
import unittest
from itertools import chain, combinations

spaceDim = 2
useConformingTraces = True
mu = 1.0
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
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
combos = combinations([-1.,1.,0.,.5,-.5,.25,-.25,.75,-.75,.8,-.8,.1,-.1,.2,-.2,.3,-.3,.4,-.4,.6,-.6,.7,-.7,.8,-.8,.9,-.9,.15,-.15,.35,-.35,.45,-.45,.55,-.55,.65,-.65,.85,-.85,.95,-.95,.125,-.125,.175,-.175,.225,-.225,.275,-.275,.325,-.325,.375,-.375,.425,-.425,.475,-.475,.525,-.525,.575,-.575,.625,-.625,.675,-.675,.725,-.725,.825,-.825,.875,-.875,.925,-.925,.975,-.975,.33,-.33,.66,-.66],2)
refCellVertexPoints = []
for e in combos:
    refCellVertexPoints.append(list(e))



class TestPlotter(unittest.TestCase):

    """Test plotMesh"""
    def test_plotMesh(self):
        print "Plot_Mesh"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        CellIDs = []
        for i in range(0,mesh.numElements()):
            CellIDs.append(i)

        #print CellIDs

        plotMesh(CellIDs,mesh)
    
    """Test plot Mesh Refine"""
    def test_plotRefineMesh(self):
        print "Plot_RefineMesh"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        mesh.hRefine([0])

        CellIDs = []
        for i in range(0,mesh.numElements()):
            CellIDs.append(i)

        #print CellIDs

        plotMesh(CellIDs,mesh)

    """ Test Plot"""
    def test_plot_u1(self):
        print "Plot_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
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
        form = None
    
    """ Test Plot with p auto refine"""
    def test_plotPAutoRefine_u1(self): 
        print "pAutoRefine_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
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

        form = None

    """ Test Plot with h auto refine"""
    def test_plothAutoRefine_u1(self):    
        print "hAutoRefine_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
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

        form = None

    """ Test Plot with p manual refine"""
    def test_plotpManualRefine_u1(self): 
        print "pManualRefine_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()


        mesh = form.solution().mesh();
        activeCellIDs = mesh.getActiveCellIDs()
        #print "pManual: "+str(activeCellIDs)
        mesh.pRefine([3,1])

        u1_soln = Function.solution(form.u(1),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

        form = None

    """ Test Plot with h manual refine"""
    def test_plothManualRefine_u1(self): 
        #return
        print "hManualRefine_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()


        mesh = form.solution().mesh();
        activeCellIDs = mesh.getActiveCellIDs()
        #print "hManual: "+str(activeCellIDs)
        mesh.hRefine([0,1])

        u1_soln = Function.solution(form.u(1),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

        form = None

    """ Test Plot"""
    def test_plot_u2(self):
        print "Plot_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()

        u2_soln = Function.solution(form.u(2),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u2_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)
        form = None
    
    """ Test Plot with p auto refine"""
    def test_plotPAutoRefine_u2(self): 
        print "pAutoRefine_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
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

        u2_soln = Function.solution(form.u(2),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u2_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

        form = None

    """ Test Plot with h auto refine"""
    def test_plothAutoRefine_u2(self):    
        print "hAutoRefine_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
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

        u2_soln = Function.solution(form.u(2),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u2_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

        form = None

    """ Test Plot with p manual refine"""
    def test_plotpManualRefine_u2(self): 
        print "pManualRefine_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()


        mesh = form.solution().mesh();
        activeCellIDs = mesh.getActiveCellIDs()
        #print "pManual: "+str(activeCellIDs)
        mesh.pRefine([3,1])

        u2_soln = Function.solution(form.u(2),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u2_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

        form = None

    """ Test Plot with h manual refine"""
    def test_plothManualRefine_u2(self): 
        #return
        print "hManualRefine_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        energyError = form.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()


        mesh = form.solution().mesh();
        activeCellIDs = mesh.getActiveCellIDs()
        #print "hManual: "+str(activeCellIDs)
        mesh.hRefine([0,1])

        u2_soln = Function.solution(form.u(2),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = u2_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)

        form = None


    if __name__ == '__main__':
        unittest.main()
