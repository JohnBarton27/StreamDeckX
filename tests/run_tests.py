import pathlib
import sys
import unittest
import xmlrunner

# Set PYTHONPATH
sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute().parent.absolute().joinpath('streamdeckx')))

test_dir = pathlib.Path(__file__).parent.absolute()
loader = unittest.TestLoader()
suite = loader.discover(test_dir)

runner = xmlrunner.XMLTestRunner("test-reports")
results = runner.run(suite)
if results.errors or results.failures:
    raise Exception('Found unit test failures!')
