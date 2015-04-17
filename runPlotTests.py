from TestPlotter import *
from TestPlotterError import *
from TestPlotterP import *
from TestPlotterStream import *

import unittest

testSuite = unittest.makeSuite(TestPlotterError)
#testSuite.addTest(unittest.makeSuite(TestPlotterError))
#testSuite.addTest(unittest.makeSuite(TestPlotterP))
#testSuite.addTest(unittest.makeSuite(TestPlotterStream))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
