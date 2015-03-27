from TestFunctionParser import *
from TestConditionParser import *
#from TestMementoExc import * 
import unittest

testSuite = unittest.makeSuite(TestFunctionParser)
testSuite.addTest(unittest.makeSuite(TestConditionParser))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
