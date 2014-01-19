import glob
import unittest

test_file_strings = glob.glob('*.py')
test_file_strings.remove('__init__.py')
test_file_strings.remove('basetest.py')
test_file_strings.remove('suite.py')

module_strings = [f[0:-3] for f in test_file_strings]
suites = [unittest.defaultTestLoader.loadTestsFromName(f) for f
          in module_strings]
testSuite = unittest.TestSuite(suites)
text_runner = unittest.TextTestRunner().run(testSuite)
