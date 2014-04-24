import os
import inspect
from requests import Session

from aipom import ApiTestCase

from tests.fixtures import Fixtures
from tests.auth import get_token
from tests.settings import SERVER_URL, PRINT_PAYLOAD, PRINT_URL

session = Session()
token = get_token(session=session)
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
fixtures = Fixtures(os.path.join(PWD, './fixtures.json'),
                    session=session, token=token)


class SuperdeskTestCase(ApiTestCase):

    session = session
    token = token

    maxDiff = None
    server_url = SERVER_URL.rstrip('/')

    print_url = PRINT_URL
    print_payload = PRINT_PAYLOAD

    def request(self, method, uri, *args,
                with_auth=True, token=None,
                add_server=True, **kwargs):

        if 'headers' in kwargs:
            headers = kwargs.pop('headers')
        else:
            headers = {}

        if with_auth:
            if not token:
                if not self.token:
                    self.token = get_token(session=self.session)
                token = self.token
            headers.update({'Authorization': token})

        super(SuperdeskTestCase, self).request(
            method, uri, *args,
            headers=headers, add_server=add_server, **kwargs)
