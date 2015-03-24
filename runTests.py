from TestFunctionParser import *
#from TestMementoExc import * 
import unittest

testSuite = unittest.makeSuite(TestFunctionParser)
#testSuite.addTest(unittest.makeSuite(Test))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
