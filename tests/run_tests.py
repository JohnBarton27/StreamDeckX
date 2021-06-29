import pathlib
import unittest
import xmlrunner

test_dir = pathlib.Path(__file__).parent.absolute()
loader = unittest.TestLoader()
suite = loader.discover(test_dir)

runner = xmlrunner.XMLTestRunner("test-reports")
runner.run(suite)
