from PyCamellia import *
from InputData import *
import SolutionFns
import unittest


useConformingTraces = True
mu = 1.0
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
polyOrderNum = 3
delta_k = 1
re = 1000.0
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
nStokesInputData = InputData(nStokes)
stokesInputData = InputData(stokes)
form = steadyLinearInit(dims, numElements, polyOrderNum)
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
        dataMap = memento.get()
        self.assertIn("stokes", dataMap)
        self.assertNotIn("nStokes", dataMap)
        
        memento.set([nStokes])
        dataMap = memento.get()
        self.assertIn(nStokes, dataMap)
        self.assertNotIn(stokes, dataMap)

    """Test InputData's init"""
    def test_inputDataInit(self):
        inputData = InputData(stokes)
        self.assertIsNotNone(inputData)
        self.assertEqual(stokes, inputData.getVariable("stokes"))

    """Test InputData's setForm & getForm"""
    def test_inputDataSetGetForm(self):
        inputData = InputData(stokes)
        inputData.setForm(form)
        self.assertIs(form, inputData.getForm())

    """Test InputData's addVariable & getVariable"""
    def test_inputDataAddVariable(self):
        inputData = InputData(stokes)
        inputData.addVariable(transient, transient)
        self.assertEqual(stokes, inputData.getVariable("stokes"))
        self.assertEqual(transient, inputData.getVariable("transient"))

    """Test InputData's createMemento"""
    def test_inputDataCreateMemento(self):
        inputData = InputData(stokes)
        memento = inputData.createMemento()
        self.assertIsNotNone(memento)
        self.assertIn("stokes", memento.get())

    """Test InputData's setMemento"""
    def test_inputDataSetMemento(self):
        inputData = InputData(stokes)
        inputData.setForm(form)
        inputData.addVariable("transient", transient)
        inputData.addVariable("dims", dims)
        inputData.addVariable("numElements", numElements)
        inputData.addVariable("mesh", meshTopo)
        inputData.addVariable("polyOrder", polyOrder)
        memento = inputData.createMemento()
        
        newData = InputData(nStokes)
        newData.setMemento(memento)
        mementoNew = newData.createMemento()
        dataMap = memento.get()
        self.assertIs(inputData.getForm(), newData.getForm())
        self.assertIn("form", dataMap)
        self.assertIn("stokes", dataMap)
        self.assertNotIn("nStokes", dataMap)
        self.assertIn("transient", dataMap)
        self.assertIn("dims", dataMap)
        self.assertIn("numElements", dataMap)
        self.assertIn("mesh", dataMap)
        self.assertIn("polyOrder", dataMap)

    """Test Reynold's init"""
    def test_reynoldsInit(self):
        self.assertIsNotNone(reynolds)

    """Test Reynold's prompt"""
    def test_reynoldsPrompt(self):
        pass

    """Test Reynold's store with a good value"""
    def test_reynoldsStoreGoodVal(self):
        success = reynolds.store(nStokesInputData, re)
        self.assertTrue(success)
        self.assertEqual(re, nStokesInputData.getVariable("reynolds"))

    """Test Reynold's store with a bad value"""
    def test_reynoldsStoreBadVal(self):
        success = reynolds.store(nStokesInputData, "not an integer")
        self.assertFalse(success)

    """Test Reynold's hasNext"""
    def test_reynoldsHasNext(self):
        self.assertTrue(reynolds.hasNext())

    """Test Reynold's next"""
    def test_reynoldsNext(self):
        self.assertEqual(reynolds.next(), state)

    """Test State's init"""
    def test_stateInit(self):
        self.assertIsNotNone(state)

    """Test State's prompt"""
    def test_statePrompt(self):
        pass

    """Test State's store a good value"""
    def test_stateStoreGoodVal(self):
        success = state.store(nStokesInputData, steadyState)
        self.assertTrue(success)
        self.assertEqual(steadyState, nStokesInputData.getVariable("steady state"))
        
        stokesInputData = InputData(stokes)
        success = state.store(stokesInputData, transient)
        self.assertTrue(success)
        self.assertEqual(transient, stokesInputData.getVariable("transient"))
        success = state.store(stokesInputData, steadyState)
        self.assertTrue(success)
        self.assertEqual(steadyState, stokesInputData.getVariable("steady state"))

    """Test State's store a bad value"""
    def test_stateStoreBadVal(self):
        success = state.store(nStokesInputData, 0)
        self.assertFalse(success)
        success = state.store(nStokesInputData, transient)
        self.assertFalse(success)

    """Test State's hasNext"""
    def test_stateHasNext(self):
        self.assertTrue(state.hasNext())

    """Test State's next"""
    def test_stateNext(self):
        self.assertEqual(state.next(), meshDims)

    """Test State's undo"""
    def test_stateUndo(self):
        self.assertEqual(reynolds, state.undo())

    """Test MeshDimensions's init"""
    def test_meshDimensionsInit(self):
        self.assertIsNotNone(meshDims)

    """Test MeshDimensions's prompt"""
    def test_meshDimensionsPrompt(self):
        pass

    """Test MeshDimensions's store a good value"""
    def test_meshDimensionsStoreGoodVal(self):
        success = meshDims.store(nStokesInputData, "1.0 x 1.0")
        self.assertTrue(success)
        self.assertEqual(dims, nStokesInputData.getVariable("meshDimensions"))

    """Test MeshDimensions's store a bad value"""
    def test_meshDimensionsStoreBadVal(self):
        success = meshDims.store(nStokesInputData, "not a floating point value")
        self.assertFalse(success)
        success = meshDims.store(nStokesInputData, 0)
        self.assertFalse(success)

    """Test MeshDimensions's hasNext"""
    def test_meshDimensionsHasNext(self):
        self.assertTrue(meshDims.hasNext())

    """Test MeshDimensions's next"""
    def test_meshDimensionsNext(self):
        self.assertEqual(meshDims.next(), elements)

    """Test MeshDimensions's undo"""
    def test_meshDimensionsUndo(self):
        self.assertEqual(state, meshDims.undo())

    """Test Elements' init"""
    def test_elementsInit(self):
        self.assertIsNotNone(elements)

    """Test Elements' prompt"""
    def test_elementsPrompt(self):
        pass

    """Test Elements' store good value"""
    def test_elementsStoreGoodVal(self):
        success = elements.store(nStokesInputData, "2 x 2")
        self.assertTrue(success)
        self.assertEqual(numElements, nStokesInputData.getVariable("numElements"))

    """Test Elements' store bad value"""
    def test_elementsStoreBadVal(self):
        success = elements.store(nStokesInputData, "not an integer")
        self.assertFalse(success)
        success = elements.store(nStokesInputData, 0.)
        self.assertFalse(success)

    """Test Elements' hasNext"""
    def test_elementsHasNext(self):
        self.assertTrue(elements.hasNext())

    """Test Elements' next"""
    def test_elementsNext(self):
        self.assertEqual(elements.next(), polyOrder)

    """Test Elements' undo"""
    def test_elementsUndo(self):
        self.assertEqual(meshDims, elements.undo())

    """Test PolyOrder's init"""
    def test_polyOrderInit(self):
        self.assertIsNotNone(polyOrder)

    """Test PolyOrder's prompt"""
    def test_polyOrderPrompt(self):
        pass

    """Test PolyOrder's store good value"""
    def test_polyOrderStoreGoodVal(self):
        success = polyOrder.store(nStokesInputData, polyOrderNum)
        self.assertTrue(success)
        self.assertEqual(polyOrderNum, nStokesInputData.getVariable("polyOrder"))

    """Test PolyOrder's store bad value"""
    def test_polyOrderStoreBadVal(self):
        success = polyOrder.store(nStokesInputData, "not an integer")
        self.assertFalse(success)
        success = polyOrder.store(nStokesInputData, 10)
        self.assertFalse(success)
        sucess = polyOrder.store(nStokesInputData, 5.0)
        self.assertFalse(success)

    """Test PolyOrder's hasNext"""
    def test_polyOrderHasNext(self):
        self.assertTrue(polyOrder.hasNext())

    """Test PolyOrder's next"""
    def test_polyOrderNext(self):
        self.assertEqual(polyOrder.next(), inflow)

    """Test PolyOrder's undo"""
    def test_polyOrderUndo(self):
        self.assertEqual(elements, polyOrder.undo())

    """Test Inflow's init"""
    def test_inflowInit(self):
        self.assertIsNotNone(inflow)

    """Test Inflow's prompt"""
    def test_inflowPrompt(self):
        pass

    """Test Inflow's store good value"""
    def test_inflowStoreGoodVal(self):
        pass

    """Test Inflow's store bad value"""
    def test_inflowStoreBadVal(self):
        pass

    """Test Inflow's obtainData"""
    def test_inflowObtainData(self):
        pass

    """Test Inflow's hasNext"""
    def test_inflowHasNext(self):
        self.assertTrue(inflow.hasNext())

    """Test Inflow's next"""
    def test_inflowNext(self):
        self.assertEqual(inflow.next(), outflow)

    """Test Inflow's undo"""
    def test_inflowUndo(self):
        self.assertEqual(polyOrder, inflow.undo())

    """Test Outflow's init"""
    def test_outflowInit(self):
        self.assertIsNotNone(outflow)

    """Test Outflow's prompt"""
    def test_outflowPrompt(self):
        pass

    """Test Outflow's store good value"""
    def test_outflowStoreGoodVal(self):
        pass

    """Test Outflow's store bad value"""
    def test_outflowStoreBadVal(self):
        pass

    """Test Outflow's obtaindata"""
    def test_outflowObtainData(self):
        pass

    """Test Outflow's hasNext"""
    def test_outflowHasNext(self):
        self.assertTrue(outflow.hasNext())

    """Test Outflow's next"""
    def test_outflowNext(self):
        self.assertEqual(outflow.next(), walls)

    """Test Outflow's undo"""
    def test_outflowUndo(self):
        self.assertEqual(inflow, outflow.undo())

    """Test Walls's init"""
    def test_wallsInit(self):
        self.assertIsNotNone(walls)

    """Test Walls's prompt"""
    def test_wallsPrompt(self):
        pass

    """Test Walls's store good value"""
    def test_wallsStoreGoodVal(self):
        pass

    """Test Walls's store bad value"""
    def test_wallsStoreBadVal(self):
        pass

    """Test Walls's obtainData"""
    def test_wallsObtainData(self):
        pass

    """Test Walls's hasNext"""
    def test_wallsHasNext(self):
        self.assertFalse(walls.hasNext())

    """Test Walls's undo"""
    def test_wallsUndo(self):
        self.assertEqual(outflow, walls.undo())

    if __name__ == '__main__':
        unittest.main()




