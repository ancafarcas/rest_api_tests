import json
from requests import Session

from api_test_tool.settings import SERVER_URL
from api_test_tool.auth import log_in


class FixturesException(Exception):
    pass


class Fixtures():
    server_url = SERVER_URL.rstrip('/')
    fixtures = {}
    session = None
    token = None
    
    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self.fixtures = json.loads(f.read())
        except Exception:
            raise FixturesException("Fixture file can't be loaded")
        self.session = Session()
        self.token = log_in(session = self.session)

    def reset_app(self):
        resp = self.session.request('PUT', self.server_url)
        if resp.text != '' or resp.status_code != 200:
            raise FixturesException("Can't reset app.")
