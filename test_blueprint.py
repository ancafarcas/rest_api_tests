import requests
from unittest import TestCase
from unittest import main as start_tests
from xmlrunner import XMLTestRunner

from blueprint_testgen import meta_BlueprintTest
from api_testclass import ApiTestCase, ApiTestRunner
from auth import log_in
from settings import XML_OUTPUT, VERBOSITY


if XML_OUTPUT:
    test_runner = XMLTestRunner
else:
    test_runner = ApiTestRunner


class BlueprintTestCase(TestCase, ApiTestCase, metaclass=meta_BlueprintTest):

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.session = requests.Session()
        cls.token = log_in(session=cls.session)


if __name__ == '__main__':
    start_tests(verbosity=VERBOSITY, testRunner=test_runner)
