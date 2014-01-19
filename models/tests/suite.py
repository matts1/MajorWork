import glob
import unittest
import sys

test_file_strings = glob.glob('*.py')
test_file_strings.remove('__init__.py')
test_file_strings.remove('basetest.py')
test_file_strings.remove('suite.py')

module_strings = [str[0:-3] for str in test_file_strings]
suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str
           in module_strings]
testSuite = unittest.TestSuite(suites)
text_runner = unittest.TextTestRunner().run(testSuite)
