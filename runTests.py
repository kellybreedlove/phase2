from TestFunctionParser import *
from TestConditionParser import * 
#from TestInputData import *
from TestPlotter import *
import unittest

testSuite = unittest.makeSuite(TestFunctionParser)
#testSuite.addTest(unittest.makeSuite(TestInputData))
testSuite.addTest(unittest.makeSuite(TestPlotter))
#testSuite.addTest(unittest.makeSuite(TestConditionParser))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
