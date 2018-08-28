import unittest
from testdb import TestDB

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDB))

runner = unittest.TextTestRunner()
runner.run(suite)