from TestFunctionParser import *
from TestConditionParser import * 
import unittest

testSuite = unittest.makeSuite(TestFunctionParser)
#testSuite.addTest(unittest.makeSuite(TestConditionParser))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
