import json
from requests import Session

from api_test_tool.settings import SERVER_URL
from api_test_tool.auth import log_in


class FixturesException(Exception):
    pass


class Fixtures():
    server_url = SERVER_URL.rstrip('/')
    fixtures = {}
    generated = {}
    session = None
    token = None
    
    def __init__(self, file_path, session=None, token=None):
        try:
            with open(file_path, 'r') as f:
                self.fixtures = json.loads(f.read())
        except Exception:
            raise FixturesException("Fixture file can't be loaded")
        self.generated = {path: [] for path in self.fixtures}
        if session:
            self.session = session
        else:
            self.session = Session()
        if token:
            self.token = token
        else:
            self.token = log_in(session = self.session)

    def _upload_record(self, path, record):
        resp = self.session.post(self.server_url + path, verify=False,
                                 headers={'Authorization': self.token},
                                 data=json.dumps(record))
        #print(resp.text)
        #print(resp.status_code)
        if resp.status_code != 201:
            raise FixturesException("Can't upload record.",
                                    resp.status_code, resp.text)

    def get(self, path):
        return self.fixtures[path]["preloaded_data"] + self.generated[path]

    def last_id(self, path):
        return len(self.get(path))

    def number(self, path):
        return len(self.fixtures[path]["preloaded_data"]) \
+ self.fixtures[path]["default_number"]

    def reset_app(self):
        resp = self.session.put(self.server_url, verify=False,
                                headers={'Authorization': self.token})
        if resp.text != '' or resp.status_code != 200:
            raise FixturesException("Can't reset app.",
                                    resp.status_code, resp.text)

    def generate(self, path, number):
        if "template" not in self.fixtures[path]:
            raise FixturesException("No template.")
        template = self.fixtures[path]["template"]
        for index in range(1, number+1):
            record = {key: value.format(n=index) for key, value
                      in template.items()}
            self._upload_record(path, record)
            self.generated[path].append(record)

    def upload(self, path):
        fixture = self.fixtures[path]
        if "fixtures" in fixture:
            for record in fixture["fixtures"]:
                self._upload_record(path, record)
        if "default_number" in fixture:
            self.generate(path, fixture["default_number"])

    def init(self, path):
        self.reset_app()
        self.upload(path)

    def init_all(self):
        for path in self.fixtures:
            self.init(path)
