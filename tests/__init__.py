import os

from api_test_tool import Fixtures


PWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
fixtures = Fixtures(os.path.join(PWD, './fixtures.json'))
