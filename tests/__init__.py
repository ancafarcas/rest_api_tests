import os
import inspect
from requests import Session

from api_test_tool import Fixtures, log_in

session = Session()
token = log_in(session=session)
PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
fixtures = Fixtures(os.path.join(PWD, './fixtures.json'),
                    session=session, token=token)
