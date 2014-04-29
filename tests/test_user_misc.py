from tests import fixtures, SuperdeskTestCase
import hashlib
from os.path import os

class UserMiscTestCase(SuperdeskTestCase):

    @classmethod
    def uri(cls, obj_id):
        return '/HR/User/{id}'.format(id=obj_id)

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

    def test_delete_user(self):
        # check user is here
        self.GET(self.uri(self.record_id))
        self.expect_status(200)

        # delete success
        self.DELETE(self.uri(self.record_id))
        self.expect_status(204)
 
        # delete again same response?
        self.DELETE(self.uri(self.record_id))
        self.expect_status(204)
 
        # check user not exists
        self.GET(self.uri(self.record_id))
        self.expect_status(404)
