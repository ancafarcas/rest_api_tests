from api_test_tool import ApiTestCase
from tests import fixtures, session, token


class UserSearchListTestCase(ApiTestCase):
    session = session
    token = token

    @classmethod
    def setUpClass(cls):
        fixtures.init('/HR/User', number=5)
        cls.number_of_users = fixtures.number('/HR/User')

    def test_list_user(self):
        # first element
        self.GET('/HR/User?maxResults=1')
        self.expect_status(200)
        self.expect_json(
            {'collection':
             [
                 {'href': self.get_url('/api-test/HR/User/1')}
             ],
             'last': self.get_url('/api-test/HR/User/?maxResults=1&offset=6'),
             'maxResults': 1,
             'next': self.get_url('/api-test/HR/User/?maxResults=1&offset=1'),
             'offset': 0,
             'total': 7}
        )
        # last element
        self.GET('/HR/User?offset=6')
        self.expect_status(200)
        self.expect_json({
            'collection':
            [{'href': self.get_url('/api-test/HR/User/7')}],
            'maxResults': 30,
            'offset': 6,
            'total': 7})
        # all without first two and last two
        self.GET('/HR/User?maxResults=3&offset=2')
        self.expect_status(200)
        self.expect_json({
            'collection': [
                {'href': self.get_url('/api-test/HR/User/3')},
                {'href': self.get_url('/api-test/HR/User/4')},
                {'href': self.get_url('/api-test/HR/User/5')}],
            'last': self.get_url('/api-test/HR/User/?maxResults=3&offset=4'),
            'maxResults': 3,
            'next': self.get_url('/api-test/HR/User/?maxResults=3&offset=5'),
            'offset': 2,
            'total': 7})

    def test_search_success(self):
        fixtures.generate('/HR/User', 5)
        # search by first name
        self.GET(
            '/HR/User?all=%25rname1%25',
            headers={'X-Filter': 'User.Id,User.FirstName'})
        self.expect_status(200)
        self.expect_json({
            'collection': [{
                'FirstName': 'surname1',
                'Id': 2,
                'href': self.get_url('/api-test/HR/User/2')}],
            'maxResults': 30,
            'offset': 0,
            'total': 1})

        # search by last name
        self.GET(
            '/HR/User?all=%25name3%25',
            headers={'X-Filter': 'User.Id,User.LastName'})
        self.expect_status(200)
        self.expect_json({
            'collection': [{
                'Id': 4,
                'LastName': 'name3',
                'href': self.get_url('/api-test/HR/User/4')}],
            'maxResults': 30,
            'offset': 0,
            'total': 1})

        # search by user name
        self.GET(
            '/HR/User?all=%25test4%25',
            headers={'X-Filter': 'User.Id,User.UserName'})
        self.expect_status(200)
        self.expect_json({
            'collection': [{
                'Id': 5,
                'UserName': 'test4',
                'href': self.get_url('/api-test/HR/User/5')}],
            'maxResults': 30,
            'offset': 0,
            'total': 1})

        # search by email
        self.GET(
            '/HR/User?all=%25est5@ex%25',
            headers={'X-Filter': 'User.Id,User.EMail'})
        self.expect_status(200)
        self.expect_json({
            'collection': [{
                'EMail': 'test5@example.com',
                'Id': 6,
                'href': self.get_url('/api-test/HR/User/6')}],
            'maxResults': 30,
            'offset': 0,
            'total': 1})

        # search by phone
        self.GET(
            '/HR/User?all=%25323%25',
            headers={'X-Filter': 'User.Id,User.PhoneNumber'})
        self.expect_status(200)
        self.expect_json({
            'collection': [{
                'Id': 4,
                'PhoneNumber': '+3234567890',
                'href': self.get_url('/api-test/HR/User/4')}],
            'maxResults': 30,
            'offset': 0,
            'total': 1})

    def test_search_no_results(self):
        # search by first name
        self.GET(
            '/HR/User?all=%25rname1%25',
            headers={'X-Filter': 'User.Id,User.FirstName'})
        self.expect_status(200)
        self.expect_json({
            'collection': [],
            'maxResults': 30,
            'offset': 0,
            'total': 0})

    def test_all_users_details(self):
        self.GET('/HR/User', headers={'X-Filter': 'User.Id,User.LastName'})
        self.expect_status(200)

        self.expect_json(self.number_of_users, 'total')
        self.expect_json_length(self.number_of_users, path='collection')
