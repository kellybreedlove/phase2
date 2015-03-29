from PyCamellia import *
from Solver import *
from InputData import *
from DataUtils import *
import unittest

phase2 = Solver()
init = InitState.Instance()
create = CreateState.Instance()
stokes = StokesState.Instance()
nstokes = NavierStokesState.Instance()
post = PostSolveState.Instance()
plot = PlotState.Instance()
refine = RefineState.Instance()
load = LoadState.Instance()
save = SaveState.Instance()

href = HRefine.Instance()
pref = PRefine.Instance()

walls = Walls.Instance()
outflow = Outflow.Instance()
mesh = MeshDimensions.Instance()
state = State.Instance()

class TestSolver(unittest.TestCase):


    """Test Solver Init"""
    def test_solver(self):
        pass

    """Test InitState's Act"""
    def test_InitStateAct(self):
        self.assertEqual(init.act("create", phase2),create)
        self.assertEqual(init.act("load", phase2),load)
        self.assertEqual(init.act("other", phase2),init)
        
    """Test CreateState's Act"""
    def test_CreateStateAct(self):
        self.assertEqual(create.act("create", phase2),create)
        self.assertEqual(create.act("navier-stokes", phase2),nstokes)
        self.assertEqual(create.act("undo", phase2),init)
        self.assertEqual(create.act("other", phase2),create)
        self.assertEqual(create.act("stokes", phase2),stokes)

    """Test StokesState's Act"""
    def test_StokesStateAct(self):
        self.assertEqual(stokes.act("undo", phase2),create)
        self.assertEqual(stokes.act("transient", phase2),stokes)
        self.assertEqual(stokes.inputState, mesh)
        stokes.inputState=walls
        self.assertEqual(stokes.act("undo", phase2), stokes)
        self.assertEqual(stokes.inputState, outflow)
        self.assertEqual(stokes.act("other", phase2),stokes)
        self.assertEqual(stokes.inputState, outflow)
        
    """Test NavierStokesState's Act"""
    def test_NavierStokesStateAct(self):
        self.assertEqual(nstokes.act("undo", phase2),create)
        self.assertEqual(nstokes.act("800", phase2),nstokes)
        self.assertEqual(nstokes.inputState, state)
        nstokes.inputState=walls
        self.assertEqual(nstokes.act("undo", phase2), nstokes)
        self.assertEqual(nstokes.inputState, outflow)
        self.assertEqual(nstokes.act("other", phase2), nstokes)
        self.assertEqual(nstokes.inputState, outflow)

    """Test PostSolveState's Act"""
    def test_PostSolveStateAct(self):
        self.assertEqual(post.act("plot", phase2), plot)
        self.assertEqual(post.act("refine", phase2), refine)
        self.assertEqual(post.act("save", phase2), save)
        self.assertEqual(post.act("load", phase2), load)
        self.assertEqual(post.act("other", phase2), post)
        
    """Test PlotState's Act"""
    def test_PlotStateAct(self):
        pass

    """Test RefineState's Act"""
    def test_RefineStateAct(self):
        self.assertEqual(refine.act("h", phase2), href)
        self.assertEqual(refine.act("p", phase2), pref)
        self.assertEqual(refine.act("other", phase2), refine)

    """Test LoadState's Act"""
    def test_LoadStateAct(self):
        self.test_SaveStateAct()
        self.assertEqual(load.act("filename", phase2), post)

    """Test SaveState's Act"""
    def test_SaveStateAct(self):
        phase2.inputData = InputData(True)
        phase2.inputData.setForm(generateForm("steady"))
        phase2.inputData.addVariable("transient", False)
        phase2.inputData.addVariable("meshDimensions", dims)
        phase2.inputData.addVariable("numElements", numElements)
        phase2.inputData.addVariable("polyOrder",  polyOrder)
        phase2.inputData.addVariable("numInflows",  1)
        phase2.inputData.addVariable("inflowRegions",  [inflowRegion])
        phase2.inputData.addVariable("inflowX",  [inflowX])
        phase2.inputData.addVariable("inflowY",  [inflowY])
        phase2.inputData.addVariable("numOutflows",  1)
        phase2.inputData.addVariable("outflowRegions",  [outflowRegion])
        phase2.inputData.addVariable("numWalls",  1)
        phase2.inputData.addVariable("wallRegions",  [wallRegion])

        self.assertEqual(save.act("filename", phase2), post)


    if __name__ == '__main__':
        unittest.main()
