from api_test_tool import ApiTestCase, log_in
from api_test_tool.auth import hash_token
from api_test_tool.settings import LOGIN, PASS


class UserAuthTestCase(ApiTestCase):

    def test_login_incorrect_username(self):
        self.POST('/Security/Authentication', with_auth=False)
        self.POST('/Security/Login',
                  {'UserName': 'wrong_username',
                   'Token': self.json_response['Token'],
                   'HashedToken': hash_token(
                       'wrong_username', PASS, self.json_response['Token'])},
                  with_auth=False)
        self.expect_status(400)
        self.expect_json(
            {"other": {"invalid": {"msg": "Invalid credentials"}}})

    def test_login_incorrect_password(self):
        self.POST('/Security/Authentication', with_auth=False)
        self.POST('/Security/Login',
                  {'UserName': LOGIN,
                   'Token': self.json_response['Token'],
                   'HashedToken': hash_token(
                       LOGIN, 'wrong_password', self.json_response['Token'])},
                  with_auth=False)
        self.expect_status(400)
        self.expect_json(
            {"other": {"invalid": {"msg": "Invalid credentials"}}})

    def test_login_incorrect_token(self):
        self.POST('/Security/Login',
                  {'UserName': LOGIN,
                   'Token':
                   '07e4f625f5e8f5e380b181a5f8816dfb75418dcbe1c9da4d225895ae37\
bcaf20507c15e0f78f183e25debe30ba81df1e09e379b493aec02dc194fde73e9fc71e',
                   'HashedToken': hash_token(
                       LOGIN, PASS,
                       '07e4f625f5e8f5e380b181a5f8816dfb75418dcbe1c9da4d225895\
ae37bcaf20507c15e0f78f183e25debe30ba81df1e09e379b493aec02dc194fde73e9fc71e')},
                  with_auth=False)
        self.expect_status(400)
        self.expect_json(
            {"other": {"invalid": {"msg": "Invalid credentials"}}})

    def test_login_incorrect_hashed_token(self):
        self.POST('/Security/Authentication', with_auth=False)
        self.POST('/Security/Login',
                  {'UserName': LOGIN,
                   'Token': self.json_response['Token'],
                   'HashedToken':
                   'bc6adf5c3d7367a4ae4ce3ef6abe6024cd327f5d3ddaadff400d146126\
a16f96e4ae763a1bf1a858dad4701fecc35f73785cc397ac54487d30da3313a0d7e5f4'},
                  with_auth=False)
        self.expect_status(400)
        self.expect_json(
            {"other": {"invalid": {"msg": "Invalid credentials"}}})

    def test_logout(self):
        temporary_token = log_in()
        self.DELETE(
            '/Security/Login/{token}'.format(token=temporary_token),
            token=temporary_token)
        self.expect_status(204)

        self.GET('/HR/User', token=temporary_token)
        self.expect_status(401)
        # just in case will check if it wasn't broken other token
        self.GET('/HR/User')
        self.expect_status(200)
