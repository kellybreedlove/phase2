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
    


class TestPlotterP(unittest.TestCase):
    """ Test Plot"""
    def test_plot_p(self):
        print "Plot_p"
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

        p_soln = Function.solution(form.p(),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = p_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)
        form = None
    
    """ Test Plot with p auto refine"""
    def test_plotPAutoRefine_p(self): 
        print "pAutoRefine_p"
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

        p_soln = Function.solution(form.p(),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = p_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)
        form = None

    """ Test Plot with h auto refine"""
    def test_plothAutoRefine_p(self):    
        print "hAutoRefine_p"
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

        p_soln = Function.solution(form.p(),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = p_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)
        form = None  

    """ Test Plot with p manual refine"""
    def test_plotpManualRefine_p(self): 
        print "pManualRefine_p"
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

        mesh.pRefine([3,1])

        p_soln = Function.solution(form.p(),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = p_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)
        form = None

    """ Test Plot with h manual refine"""
    def test_plothManualRefine_p(self): 
        #return
        print "hManualRefine_p"
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

        mesh.hRefine([0,1])

        p_soln = Function.solution(form.p(),form.solution())
        activeCellIDs = mesh.getActiveCellIDs()

        p = []
        v = []
        for cellID in activeCellIDs:
            (values,points) = p_soln.getCellValues(mesh,cellID,refCellVertexPoints)
        

            p.append(points)
            v.append(values)

        plot(v, p)
        form = None
