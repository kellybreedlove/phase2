from TestPlotter import *
from TestPlotterError import *
from TestPlotterP import *
import unittest

testSuite = unittest.makeSuite(TestPlotter)
testSuite.addTest(unittest.makeSuite(TestPlotterError))
testSuite.addTest(unittest.makeSuite(TestPlotterP))


testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
