from tests import fixtures, SuperdeskTestCase


class UserSearchListTestCase(SuperdeskTestCase):

    @classmethod
    def setUpClass(cls):
        fixtures.init('/HR/User', number=5)
        cls.number_of_users = fixtures.number('/HR/User')

    def test_list_user(self):
        # first element
        self.GET('/HR/User?maxResults=1')
        self.expect_status(200)
        self.expect_json({'href': self.get_url('/api-test/HR/User/1')})

        # last element
        self.GET('/HR/User?offset=6')
        self.expect_status(200)
        self.expect_json({'href': self.get_url('/api-test/HR/User/7')})

        # all without first two and last two
        self.GET('/HR/User?maxResults=3&offset=2')
        self.expect_status(200)
        #self.inspect_json()
        self.expect_json({
            'collection': [
                {'href': self.get_url('/api-test/HR/User/3')},
                {'href': self.get_url('/api-test/HR/User/4')},
                {'href': self.get_url('/api-test/HR/User/5')}]})

    def test_search_success(self):
        # search by first name
        self.GET(
            '/HR/User?all=%25rname1%25',
            headers={'X-Filter': 'User.Id,User.FirstName'})
        self.expect_status(200)
        self.expect_json({
            'FirstName': 'surname1',
            'href': self.get_url('/api-test/HR/User/2')}
        )

        # search by last name
        self.GET(
            '/HR/User?all=%25name3%25',
            headers={'X-Filter': 'User.Id,User.LastName'})
        self.expect_status(200)
        self.expect_json({
            'LastName': 'name3',
            'href': self.get_url('/api-test/HR/User/4')}
        )

        # search by user name
        self.GET(
            '/HR/User?all=%25test4%25',
            headers={'X-Filter': 'User.Id,User.UserName'})
        self.expect_status(200)
        self.expect_json({
            'LastName': 'test4',
            'href': self.get_url('/api-test/HR/User/5')}
        )

        # search by email
        self.GET(
            '/HR/User?all=%25est5@ex%25',
            headers={'X-Filter': 'User.Id,User.EMail'})
        self.expect_status(200)
        self.expect_json({
            'Email': 'test1@example.com',
            'href': self.get_url('/api-test/HR/User/6')}
        )

        # search by phone
        self.GET(
            '/HR/User?all=%25323%25',
            headers={'X-Filter': 'User.Id,User.PhoneNumber'})
        self.expect_status(200)
        self.expect_json({
            'PhoneNumber': '+3234567890',
            'href': self.get_url('/api-test/HR/User/4')}
        )

    def test_search_no_results(self):
        # search by first name
        self.GET(
            '/HR/User?all=%25rname1%25',
            headers={'X-Filter': 'User.Id,User.FirstName'})
        self.expect_status(200)
        self.expect_json({'collection': []})

    def test_all_users_details(self):
        self.GET('/HR/User', headers={'X-Filter': 'User.Id,User.LastName'})
        self.expect_status(200)

        self.expect_json(self.number_of_users, 'total')
        self.expect_json_length(self.number_of_users, path='collection')
