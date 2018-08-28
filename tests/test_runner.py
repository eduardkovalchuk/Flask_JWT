import unittest
from testdb import TestDB

suite = unittest.TestSuite()
result = unittest.TestResult()
suite.addTest(unittest.makeSuite(TestDB))

runner = unittest.TextTestRunner()
runner.run(suite)