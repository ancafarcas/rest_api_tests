import requests
from unittest import TestCase
from unittest import main as start_tests
from urllib.parse import quote

from api_testclass import ApiTestCase
from auth import log_in


class BlueprintTestCase(TestCase, ApiTestCase):

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        #auth will be here
        cls.session = requests.Session()
        cls.token = log_in(session=cls.session)

    def test_filter_by_fullname(self):
        self.GET('/HR/User/?fullName={fullname}'
                 .format(fullname=quote('Gerald Durrell')))
        print(self.response.text)

    def test_expect_json(self):
        self.GET('http://httpbin.org/get?foo=bar&bar=baz', add_server=False)
        self.expect_json({'foo': 'bar', 'bar': 'baz'}, 'args')
        self.expect_json('bar', 'args/foo')
        self.expect_json_contains({'args': {'foo': 'bar', 'bar': 'baz'}},)
        self.expect_json_contains({'args': {'foo': 'b1r', 'bar': 'b2z'}},)

if __name__ == '__main__':
    start_tests(verbosity=2)
