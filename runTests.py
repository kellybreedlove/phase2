from TestParseFunction import *
from TestConditionParser import * 
from TestInputData import *
from TestPlotter import *
from TestSolutionFns import *
from TestSolveFormulation import *
import unittest

testSuite = unittest.makeSuite(TestParseFunction)
#testSuite.addTest(unittest.makeSuite(TestInputData))
#testSuite.addTest(unittest.makeSuite(TestSolveFormulation))
testSuite.addTest(unittest.makeSuite(TestSolutionFns))
#testSuite.addTest(unittest.makeSuite(TestPlotter))
#testSuite.addTest(unittest.makeSuite(TestConditionParser))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
