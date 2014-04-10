from api_test_tool.fixtures import Fixtures


f = Fixtures('./tests/fixtures.json', token='a')
f.reset_app()
