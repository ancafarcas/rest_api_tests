import unittest
import json
import requests

from blueprint_testgen import meta_BlueprintTest
from auth import log_in


class BlueprintTestCase(unittest.TestCase, metaclass=meta_BlueprintTest):

    @classmethod
    def setUpClass(cls):
        #auth will be here
        cls.session = requests.Session()
        cls.token = log_in(session=cls.session)

if __name__ == '__main__':
    unittest.main(verbosity=2)
