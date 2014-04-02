from api_test_tool import ApiTestCase
from api_test_tool.auth import log_in, ApiAuthException
import hashlib

from tests import fixtures, session, token


class UserMiscTestCase(ApiTestCase):
    session = session
    token = token

    @classmethod
    def uri(cls, obj_id):
        return '/HR/User/{id}'.format(id=obj_id)

    @classmethod
    def href(cls, obj_id):
        return cls.server_url + cls.uri(obj_id)

    @classmethod
    def setUpClass(cls):
        cls.last_id = fixtures.number('/HR/User')
        cls.password = 'a3r546465676bgyhyyehy'
        cls.record = {
            "FirstName": "John",
            "LastName": "Doe",
            "UserName": "john12345._-'",
            "EMail": "john1.doe2@email.com",
            "Password": hashlib.sha512(
                bytes(cls.password, 'utf-8')
            ).hexdigest(),
            "PhoneNumber": "0223456789"
        }
        cls.record_href = cls.href(cls.last_id+1)
        cls.record_uri = cls.uri(cls.last_id+1)

    def setUp(self):
        fixtures.init('/HR/User')
        # add user
        self.POST('/HR/User', self.record,
                  headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': self.record["UserName"],
            'href': self.record_href
        })

    def test_delete_user(self):
        # check user is here
        self.GET(self.uri(self.last_id))
        self.expect_status(200)
        self.inspect_headers()
        self.inspect_body()

        # delete success
        self.DELETE(self.uri(self.last_id))
        self.expect_status(204)
        self.inspect_headers()
        self.inspect_body()

        # delete again same response?
        self.DELETE(self.uri(self.last_id))
        self.expect_status(204)
        self.inspect_headers()
        self.inspect_body()

        # check user not exists
        self.GET(self.uri(self.last_id))
        self.expect_status(404)

#     def test_list_user(self):
#         #search
#         #pagination
#         self.GET('/HR/User')
#         self.expect_status(200)
#         self.inspect_headers()
#         self.inspect_body()
#
#
#     def test_all_users_details(self):
#         self.GET('/HR/User', headers={'X-Filter': 'User.*'})
#         self.inspect_headers()
#         self.inspect_body()
