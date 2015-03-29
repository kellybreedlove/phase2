from PyCamellia import *
from Plotter import *
import unittest


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
refCellVertexPoints = [[-1.,-1.],[1.,-1.],[1.,1.],[-1.,1.]];

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

        cpOrder = []
        for i in range(0,mesh.numElements()):
            cpOrder.append(mesh.cellPolyOrder(i))

        plotP(cpOrder,mesh)
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

        cpOrder = []
        for i in range(0,mesh.numElements()):
            cpOrder.append(mesh.cellPolyOrder(i))

        plotP(cpOrder,mesh)
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

        cpOrder = []
        for i in range(0,mesh.numElements()):
            cpOrder.append(mesh.cellPolyOrder(i))

        plotP(cpOrder,mesh)
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

        cpOrder = []
        for i in range(0,mesh.numElements()):
            cpOrder.append(mesh.cellPolyOrder(i))

        plotP(cpOrder,mesh)
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

        cpOrder = []
        for i in range(0,mesh.numElements()):
            cpOrder.append(mesh.cellPolyOrder(i))

        plotP(cpOrder,mesh)
        form = None
