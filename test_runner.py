from unittest import TestLoader
from xmlrunner import XMLTestRunner

from aipom import ApiTestRunner
from tests.settings import XML_OUTPUT


if XML_OUTPUT:
    test_runner = XMLTestRunner
else:
    test_runner = ApiTestRunner

PATTERN = 'test*.py'
# PATTERN='*user_success*'
if __name__ == '__main__':
    tests = TestLoader().discover(start_dir='./tests', pattern=PATTERN)
    test_runner(verbosity=2).run(tests)
