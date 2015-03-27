from PyCamellia import *
from InputData import *
import SolutionFns
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
transient = "transient"
steadyState = "steady state"

topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)

stokes = True
nStokes = False
form = steadyLinearInit(spaceDim, dims, numElements, polyOrder)
reynolds = Reynolds.Instance()
state = State.Instance()
meshDims = MeshDimensions.Instance()
elements = Elements.Instance()
polyOrder = PolyOrder.Instance()
inflow = Inflow.Instance()
outflow = Outflow.Instance()
walls = Walls.Instance()

class TestInputData(unittest.TestCase):

    """Test Some Stuff"""
    def test_Stuff(self):
        pass

    """Test Memento's get & set"""
    def test_mementoGetSet(self):
        inputData = InputData(stokes)
        memento = inputData.createMemento()
        dataList = memento.get()
        self.assertIn(stokes, dataList)
        self.assertNotIn(nStokes, dataList)
        
        memento.set([nStokes])
        dataList = memento.get()
        self.assertIn(nStokes, dataList)
        self.assertNotIn(stokes, dataList)

    """Test InputData's init"""
    def test_inputDataInit(self):
        inputData = InputData(stokes)
        memento = inputData.createMemento()
        dataList = memento.get()
        self.assertIsNotNone(inputData)
        self.assertIn(stokes, dataList)

    """Test InputData's setForm & getForm"""
    def test_inputDataSetGetForm(self):
        inputData = InputData(stokes)
        inputData.setForm(form)
        self.assertIs(form, inputData.getForm())

    """Test InputData's addVariable"""
    def test_inputDataAddVariable(self):
        inputData = InputData(stokes)
        inputData.addVariable(transient)
        memento = inputData.createMemento()
        dataList = memento.get()
        self.assertIn(stokes, dataList)
        self.assertIn(transient, dataList)

    """Test InputData's createMemento"""
    def test_inputDataCreateMemento(self):
        inputData = InputData(stokes)
        memento = inputData.createMemento()
        self.assertIsNotNone(memento)
        self.assertIn(stokes, memento.get())

    """Test InputData's setMemento"""
    def test_inputDataSetMemento(self):
        inputData = InputData(stokes)
        inputData.setForm(form)
        inputData.addVariable(transient)
        inputData.addVariable(dims)
        inputData.addVariable(numElements)
        inputData.addVariable(meshTopo)
        inputData.addVariable(polyOrder)
        memento = inputData.createMemento()
        
        inputDataNew = InputData(nStokes)
        inputDataNew.setMemento(memento)
        mementoNew = inputDataNew.createMemento()
        dataList = memento.get()
        self.assertIs(inputData.getForm(), inputDataNew.getForm())
        self.assertIn(form, dataList)
        self.assertIn(stokes, dataList)
        self.assertNotIn(nStokes, dataList)
        self.assertIn(transient, dataList)
        self.assertIn(dims, dataList)
        self.assertIn(numElements, dataList)
        self.assertIn(meshTopo, dataList)
        self.assertIn(polyOrder, dataList)

    """Test Reynold's init"""
    def test_reynoldsInit(self):
        self.assertIsNotNone(reynolds)

    """Test Reynold's prompt"""
    def test_reynoldsPrompt(self):
        pass

    """Test Reynold's store"""
    def test_reynoldsStore(self):
        pass

    """Test Reynold's hasNext"""
    def test_reynoldsHasNext(self):
        pass

    """Test Reynold's next"""
    def test_reynoldsNext(self):
        pass

    """Test State's init"""
    def test_stateInit(self):
        self.assertIsNotNone(state)

    """Test State's prompt"""
    def test_statePrompt(self):
        pass

    """Test State's store"""
    def test_stateStore(self):
        pass

    """Test State's hasNext"""
    def test_stateHasNext(self):
        pass

    """Test State's next"""
    def test_stateNext(self):
        pass

    """Test MeshDimensions's init"""
    def test_meshDimensionsInit(self):
        self.assertIsNotNone(meshDims)

    """Test MeshDimensions's prompt"""
    def test_meshDimensionsPrompt(self):
        pass

    """Test MeshDimensions's store"""
    def test_meshDimensionsStore(self):
        pass

    """Test MeshDimensions's hasNext"""
    def test_meshDimensionsHasNext(self):
        pass

    """Test MeshDimensions's next"""
    def test_meshDimensionsNext(self):
        pass

    """Test Elements' init"""
    def test_elementsInit(self):
        self.assertIsNotNone(elements)

    """Test Elements' prompt"""
    def test_elementsPrompt(self):
        pass

    """Test Elements' store"""
    def test_elementsStore(self):
        pass

    """Test Elements' hasNext"""
    def test_elementsHasNext(self):
        pass

    """Test Elements' next"""
    def test_elementsNext(self):
        pass

    """Test PolyOrder's init"""
    def test_polyOrderInit(self):
        self.assertIsNotNone(polyOrder)

    """Test PolyOrder's prompt"""
    def test_polyOrderPrompt(self):
        pass

    """Test PolyOrder's store"""
    def test_polyOrderStore(self):
        pass

    """Test PolyOrder's hasNext"""
    def test_polyOrderHasNext(self):
        pass

    """Test PolyOrder's next"""
    def test_polyOrderNext(self):
        pass

    """Test Inflow's init"""
    def test_inflowInit(self):
        self.assertIsNotNone(inflow)

    """Test Inflow's prompt"""
    def test_inflowPrompt(self):
        pass

    """Test Inflow's store"""
    def test_inflowStore(self):
        pass

    """Test Inflow's hasNext"""
    def test_inflowHasNext(self):
        pass

    """Test Inflow's next"""
    def test_inflowNext(self):
        pass

    """Test Outflow's init"""
    def test_outflowInit(self):
        self.assertIsNotNone(outflow)

    """Test Outflow's prompt"""
    def test_outflowPrompt(self):
        pass

    """Test Outflow's store"""
    def test_outflowStore(self):
        pass

    """Test Outflow's hasNext"""
    def test_outflowHasNext(self):
        pass

    """Test Outflow's next"""
    def test_outflowNext(self):
        pass

    """Test Walls's init"""
    def test_wallsInit(self):
        self.assertIsNotNone(walls)

    """Test Walls's prompt"""
    def test_wallsPrompt(self):
        pass

    """Test Walls's store"""
    def test_wallsStore(self):
        pass

    """Test Walls's hasNext"""
    def test_wallsHasNext(self):
        pass

    """Test Walls's next"""
    def test_wallsNext(self):
        pass

    if __name__ == '__main__':
        unittest.main()




