from TestPlotter import *
import unittest

testSuite = unittest.makeSuite(TestPlotter)

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
