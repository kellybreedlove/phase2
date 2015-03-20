from TestLoadSave import * 
import unittest

testSuite = unittest.makeSuite(TestLoadSave)
#testSuite.addTest(unittest.makeSuite(Test))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
