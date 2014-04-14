from unittest import main as start_tests
from urllib.parse import quote
import json
import os
from hashlib import md5
from functools import partial

from api_test_tool import ApiTestCase, ApiTestRunner
from tests import fixtures, session, token


def md5sum(filename):
    filename = os.path.abspath(filename)
    try:
        with open(filename, mode='rb') as f:
            d = md5()
            for buf in iter(partial(f.read, 128), b''):
                d.update(buf)
            return d.hexdigest()
    except FileNotFoundError:
        return ''


class UserAvatarTestCase(ApiTestCase):

    source_file = './tests/test.png'
    result_file = '/tmp/output.png'

    session = session
    token = token

    def setUp(self):
        # reset app
        fixtures.init('/HR/User')
        self.last_user_uri = '/HR/User/{id}'.format(
            id=fixtures.last_id('/HR/User'))
        self.last_useravatar_uri = '/HR/UserAvatar/{id}'.format(
            id=fixtures.last_id('/HR/User'))

    def test_avatar_upload(self):
        # change avatar for first user
        print('debug==========================')
        print(self.last_useravatar_uri)
        print('===============================')
        with open(self.source_file, 'rb') as image_file:
            self.PUT(self.last_useravatar_uri, files=[
                ('model', (
                    'blob',
                    json.dumps({
                        "CropLeft": 0,
                        "CropRight": 501,
                        "CropTop": 501,
                        "CropBottom": 0
                    }),
                    'application/json')),
                ('file', (
                    'test',
                    image_file,
                    'image/png')), ])
        self.expect_status(200)
        uploaded_image_url = self.json_response['Avatar']['href']

        # check user's avatar links
        self.GET(self.last_user_uri)
        self.expect_status(200)

        useravatar_url = self.json_response['UserAvatar']['href']
        self.assertEqual(
            self.get_url(self.last_useravatar_uri),
            useravatar_url,
            "Links to avatar object not matches.")

        userimage_url = self.json_response['Avatar']['href']
        self.assertEqual(
            uploaded_image_url,
            userimage_url,
            "Links to image not matches.")

        # check image itself
        self.GET(uploaded_image_url, add_server=False, stream=True)
        self.expect_status(200)
        with open(self.result_file, 'wb') as handle:
            for block in self.response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        self.assertEqual(
            md5sum(self.source_file),
            md5sum(self.result_file),
            "Images not matches.")


# those lines shouldn't be in actual testcase:
if __name__ == '__main__':
    start_tests(verbosity=2, testRunner=ApiTestRunner)
