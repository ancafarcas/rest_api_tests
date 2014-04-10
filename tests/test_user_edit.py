from api_test_tool import ApiTestCase
from api_test_tool.auth import log_in, ApiAuthException
import hashlib

from tests import fixtures, session, token


class UserEditTestCase(ApiTestCase):
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

    def test_success(self):
        # edit with success, check new values, check login
        self.PUT(
            self.record_uri,
            """
            {
              "FirstName": "JohnChanged",
              "LastName": "DoeChanged",
              "EMail": "john1.doe2.changed@email.com",
              "Password": "aaa3r546465676bgyhyyehy",
              "PhoneNumber":"+123123456789"
            }
            """,
            headers={'X-Filter': 'User.FirstName,User.LastName,\
User.EMail,User.Password,User.PhoneNumber'}
        )
        self.expect_status(200)
        self.expect_json({
            'EMail': 'john1.doe2.changed@email.com',
            'FirstName': 'JohnChanged',
            'LastName': 'DoeChanged',
            'PhoneNumber': '+123123456789',
            'href': self.record_href
        })

    def test_username(self):
        # username shouldn't be editable
        self.PUT(self.record_uri, {"UserName": "new_user_name"})
        self.expect_status(400)

    def test_password(self):
        new_password = 'new_password'
        new_password_hashed = hashlib.sha512(
            bytes(new_password, 'utf-8')
        ).hexdigest(),
        self.PUT(
            self.record_uri,
            {'Password': new_password_hashed})
        self.expect_status(200)
        # old password shouldn't work
        with self.assertRaises(ApiAuthException):
            log_in(username=self.record["UserName"],
                   password=self.password)
        # new password should work
        try:
            log_in(username=self.record["UserName"],
                   password=new_password)
        except ApiAuthException:
            self.fail("User can't log in with the new password.")

    def test_duplicate_email(self):
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": "john2",
                "EMail": "john2.doe@email.com",
                "Password": "a3r546465676bgyhyyehy",
                "PhoneNumber": "0223456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': 'john2',
            'href': self.href(self.last_id+2)})

        self.PUT(
            self.uri(self.last_id+2),
            {"EMail": "john1.doe2@email.com"},
            headers={'X-Filter': 'User.UserName,User.EMail'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'unique':
                {'msg': 'Unique constraint failed'}
            }})

    def test_incorect_email(self):
        self.PUT(
            self.record_uri,
            {"EMail": ";john1.doe@email.com"})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'format':
                {'msg': 'Invalid EMail'}
            }})

    def test_missing_first_name(self):
        self.PUT(
            self.record_uri,
            {"FirstName": ""},
            headers={'X-Filter': 'User.UserName,User.FirstName'})
        self.expect_status(400)
        self.expect_json(
            {'FirstName': {'mandatory':
                {'msg': 'Mandatory value is missing'}
            }})

    def test_missing_last_name(self):
        self.PUT(
            self.record_uri,
            {"LastName": ""},
            headers={'X-Filter': 'User.UserName,User.LastName'})
        self.expect_status(400)
        self.expect_json(
            {'LastName': {'mandatory':
                {'msg': 'Mandatory value is missing'}
            }})

    def test_missing_email(self):
        self.PUT(
            self.record_uri,
            {"EMail": ""},
            headers={'X-Filter': 'User.UserName,User.EMail'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'mandatory':
                {'msg': 'Mandatory value is missing'}
            }})

    def test_missing_phone(self):
        self.PUT(
            self.record_uri,
            {"PhoneNumber": ''},
            headers={'X-Filter': 'User.UserName,User.PhoneNumber'})
        self.expect_status(200)
        self.expect_json({
            'PhoneNumber': '',
            'UserName': self.record["UserName"],
            'href': self.record_href
        })

    def test_deleted(self):
        self.DELETE(self.record_uri)
        self.expect_status(204)

        self.PUT(
            self.record_uri,
            {"FirstName": 'FirstName'},
            headers={'X-Filter': 'User.UserName,User.FirstName'})
        self.expect_status(404)
        self.expect_json(
            {'Id': {'other':
                {'msg': 'Unknown value'}
            }})
