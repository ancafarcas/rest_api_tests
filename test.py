import requests
from unittest import TestCase
from unittest import main as start_tests

from blueprint_testgen import meta_BlueprintTest
from api_testclass import ApiTestCase
from auth import log_in


class BlueprintTestCase(TestCase, ApiTestCase, metaclass=meta_BlueprintTest):

    @classmethod
    def setUpClass(cls):
        #auth will be here
        cls.session = requests.Session()
        cls.token = log_in(session=cls.session)

if __name__ == '__main__':
    start_tests(verbosity=2)
