from unittest import TestCase
from unittest import main as start_tests
from urllib.parse import quote

from api_test_tool import ApiTestCase, ApiTestRunner
from tests import fixtures


class ExampleTestCase(ApiTestCase):

    def test_filter_by_fullname(self):
        self.GET('/HR/User/?fullName={fullname}'
                 .format(fullname=quote('Gerald Durrell')))
        self.inspect_json()

    def test_expect_json(self):
        self.GET('http://httpbin.org/get?foo=bar&bar=baz', add_server=False)
        self.expect_json({'foo': 'bar', 'bar': 'baz'}, 'args')
        self.expect_json('bar', 'args/foo')
        self.expect_json_contains({'args': {'foo': 'bar', 'bar': 'baz'}},)
        self.expect_json_contains({'args': {'foo': 'b1r', 'bar': 'b2z'}},)

    def test_user_create_xfilter(self):
        self.POST('/HR/User',
                  """
                  {
                      "FirstName": "John",
                      "LastName": "Doe",
                      "UserName": "john12345",
                      "EMail": "john1.doe2@email.com",
                      "Password": "a3r546465676bgyhyyehy",
                      "PhoneNumber":"0223456789"
                 }
                  """,
                  headers={'X-Filter': 'User.UserName'})
        self.inspect_status()
        self.inspect_json()

    def test_fixtures(self):
        fixtures.init('/HR/User')
        self.GET('/HR/User')
        self.inspect_json()

# those lines shouldn't be in actual testcase:
if __name__ == '__main__':
    start_tests(verbosity=2, testRunner=ApiTestRunner)
