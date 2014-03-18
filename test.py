import unittest
import json
import requests

from blueprint_testgen import meta_BlueprintTest


class BlueprintTestCase(unittest.TestCase, metaclass=meta_BlueprintTest):

    @classmethod
    def setUpClass(cls):
        #auth will be here
        cls.session = requests.Session()

if __name__ == '__main__':
    unittest.main(verbosity=2)
