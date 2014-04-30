import hashlib

from tests import fixtures, SuperdeskTestCase
from tests.auth import get_token, ApiAuthException
from os.path import os

class UserAddTestCase(SuperdeskTestCase):

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

    def setUp(self):
        fixtures.init('/HR/User')
        # add user
        self.POST('/HR/User', self.record,
                  headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': self.record["UserName"]
        }, partly=True)
        
        self.record_href = self.json_response['href']
        self.record_id = int(os.path.basename(self.record_href))
        self.record_uri = self.uri(self.record_id)

    def test_success(self):
        # check if user is created
        self.GET(self.uri(self.record_id))
        self.expect_status(200)

        # log in with newly created user
        try:
            get_token(username=self.record["UserName"],
                      password=self.password),
        except ApiAuthException:
            self.fail("Newly created user can't log in.")

    def test_already_deleted(self):
        # add deleted user
        self.DELETE(self.record_uri)
        self.expect_status(204)
        self.POST('/HR/User', self.record,
                  headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json(self.record["UserName"])
 
        try:
            get_token(username=self.record["UserName"],
                      password=self.password),
        except ApiAuthException:
            self.fail("Newly created user can't log in.")
 
    def test_duplicate_username(self):
        # add duplicate username
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": "john12345._-'",
                "EMail": "john12.doe2@email.com",
                "Password": "a3r546465676bgyhyyehy",
                "PhoneNumber": "0223456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'UserName': {'conflict':
                {'msg': 'There is already an active user with this name'}
            }})
 
    def test_duplicate_email(self):
        # add duplicate email
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": "john112345",
                "EMail": "john1.doe2@email.com",
                "Password": "a3r546465676bgyhyyehy",
                "PhoneNumber": "0223456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'unique':
                {'msg': 'Unique constraint failed'}
            }})
 
    def test_incorrect_username(self):
        # add incorrect username
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": ";john112345",
                "EMail": "john13.doe2@email.com",
                "Password": "a3r546465676bgyhyyehy",
                "PhoneNumber": "0223456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'UserName': {'user name':
                {'msg': 'Invalid user name format',
                 'example': 'The user name must contain only letters, \
digits and characters ".", "_", "\'", "-"'}
            }})

    def test_incorrect_email(self):
        # add incorrect email
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": "john112345",
                "EMail": ";john13.doe2@email.com",
                "Password": "a3r546465676bgyhyyehy",
                "PhoneNumber": "0223456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'format':
                {'msg': 'Invalid EMail'}
            }})
 
    def test_missing_first_name(self):
        # add missing first name
        self.POST(
            '/HR/User',
            {
                "LastName": "Doe",
                "UserName": "johnfirst",
                "EMail": "john.doe.first@email.com",
                "Password": "a3r546465676bgyhyyehy",
                "PhoneNumber": "0223456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'FirstName': {'mandatory':
                {'msg': 'Mandatory value is missing'}
            }})

    def test_missing_last_name(self):
        # add missing last name
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "UserName": "johnlast",
                "EMail": "john.doe.last@email.com",
                "Password": "a3r546465676bgyhyyehy",
                "PhoneNumber": "0223456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'LastName': {'mandatory':
                {'msg': 'Mandatory value is missing'}
            }})

    def test_missing_email(self):
        # add missing email
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": "johnemail",
                "Password": "a3r546465676bgyhyyehy",
                "PhoneNumber": "0223456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'EMail': {'mandatory':
                {'msg': 'Mandatory value is missing'}
            }})
 
    def test_missing_phone(self):
        # add missing phone
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": "johnphone",
                "EMail": "john.doe.phone@email.com",
                "Password": "a3r546465676bgyhyyehy",
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(201)
        self.expect_json({
            'UserName': "johnphone",
            'href': self.record_href
        })

    def test_missing_password(self):
        # missing password
        self.POST(
            '/HR/User',
            {
                "FirstName": "John",
                "LastName": "Doe",
                "UserName": "johnpassword",
                "EMail": "john.doe.password@email.com",
                "PhoneNumber": "+123123456789"
            },
            headers={'X-Filter': 'User.UserName'})
        self.expect_status(400)
        self.expect_json(
            {'Password': {'mandatory':
                {'msg': 'Mandatory value is missing'}
            }})
