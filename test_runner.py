from unittest import TestLoader
from xmlrunner import XMLTestRunner

from api_testclass import ApiTestRunner
from settings import XML_OUTPUT, VERBOSITY


if XML_OUTPUT:
    test_runner = XMLTestRunner
else:
    test_runner = ApiTestRunner


if __name__ == '__main__':
    tests = TestLoader().discover(start_dir='./tests')
    test_runner(verbosity=VERBOSITY).run(tests)
