from PyCamellia import *
from Solver import *
from InputData import *
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

href = hRefine.Instance()
pref = pRefine.Instance()

walls = Walls.Instance()
outflow = Outflow.Instance()
mesh = MeshDimensions.Instance()
state = State.Instance()

class TestSolver(unittest.TestCase):


    """Test InitState"""
    def test_InitState(self):
        self.assertEqual(init.act("create", phase2),create)
        self.assertEqual(init.act("load", phase2),load)
        self.assertEqual(init.act("other", phase2),init)
        
    """Test CreateState"""
    def test_CreateState(self):
        self.assertEqual(create.act("create", phase2),create)
        self.assertEqual(create.act("navier-stokes", phase2),nstokes)
        self.assertEqual(create.act("undo", phase2),init)
        self.assertEqual(create.act("other", phase2),create)
        self.assertEqual(create.act("stokes", phase2),stokes)

    """Test StokesState"""
    def test_StokesState(self):
        self.assertEqual(stokes.act("undo", phase2),create)
        self.assertEqual(stokes.act("transient", phase2),stokes)
        self.assertEqual(stokes.inputState, mesh)
        stokes.inputState=walls
        self.assertEqual(stokes.act("undo", phase2), stokes)
        self.assertEqual(stokes.inputState, outflow)
        self.assertEqual(stokes.act("other", phase2),stokes)
        self.assertEqual(stokes.inputState, outflow)
        
    """Test NavierStokesState"""
    def test_NavierStokesState(self):
        self.assertEqual(nstokes.act("undo", phase2),create)
        self.assertEqual(nstokes.act("800", phase2),nstokes)
        self.assertEqual(nstokes.inputState, state)
        nstokes.inputState=walls
        self.assertEqual(nstokes.act("undo", phase2), nstokes)
        self.assertEqual(nstokes.inputState, outflow)
        self.assertEqual(nstokes.act("other", phase2), nstokes)
        self.assertEqual(nstokes.inputState, outflow)

    """Test PostSolveState"""
    def test_PostSolveState(self):
        self.assertEqual(post.act("plot", phase2), plot)
        self.assertEqual(post.act("refine", phase2), refine)
        self.assertEqual(post.act("save", phase2), save)
        self.assertEqual(post.act("load", phase2), load)
        self.assertEqual(post.act("other", phase2), post)
        
    """Test RefineState"""
    def test_RefineState(self):
        self.assertEqual(refine.act("h", phase2), href)
        self.assertEqual(refine.act("p", phase2), pref)
        self.assertEqual(refine.act("other", phase2), refine)


    if __name__ == '__main__':
        unittest.main()
