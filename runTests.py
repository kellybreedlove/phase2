from TestConditionParser import * 
from TestInputData import *
from TestParseFunction import * 
from TestPlotter import *
from TestPlotterError import *
from TestPlotterP import *
from TestPlotterStream import *
from TestRefine import *
from TestSolutionFns import *
from TestSolveFormulation import *
from TestSolver import *
import unittest

testSuite = unittest.makeSuite(TestConditionParser)
testSuite.addTest(unittest.makeSuite(TestInputData))
testSuite.addTest(unittest.makeSuite(TestParseFunction))
testSuite.addTest(unittest.makeSuite(TestPlotter))
testSuite.addTest(unittest.makeSuite(TestPlotterError))
testSuite.addTest(unittest.makeSuite(TestPlotterP))
testSuite.addTest(unittest.makeSuite(TestPlotterStream))
testSuite.addTest(unittest.makeSuite(TestRefine))
testSuite.addTest(unittest.makeSuite(TestSolutionFns)) # done
testSuite.addTest(unittest.makeSuite(TestSolveFormulation)) # done
testSuite.addTest(unittest.makeSuite(TestSolver)) # done

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
