from api_test_tool import ApiTestCase
from tests import fixtures, session, token


class UserMiscTestCase(ApiTestCase):
    session = session
    token = token

    @classmethod
    def uri(cls, obj_id):
        return '/HR/User/{id}'.format(id=obj_id)

    @classmethod
    def setUpClass(cls):
        cls.last_id = fixtures.number('/HR/User')

    def setUp(self):
        fixtures.init('/HR/User')

    def test_delete_user(self):
        # check user is here
        self.GET(self.uri(self.last_id))
        self.expect_status(200)

        # delete success
        self.DELETE(self.uri(self.last_id))
        self.expect_status(204)

        # delete again same response?
        self.DELETE(self.uri(self.last_id))
        self.expect_status(204)

        # check user not exists
        self.GET(self.uri(self.last_id))
        self.expect_status(404)
