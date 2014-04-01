from unittest import TestLoader
from xmlrunner import XMLTestRunner

from api_test_tool import ApiTestRunner
from api_test_tool.settings import XML_OUTPUT, VERBOSITY


if XML_OUTPUT:
    test_runner = XMLTestRunner
else:
    test_runner = ApiTestRunner

PATTERN='test*.py'
#PATTERN='*user_success*'
if __name__ == '__main__':
    tests = TestLoader().discover(start_dir='./tests', pattern=PATTERN)
    test_runner(verbosity=VERBOSITY).run(tests)
