from unittest import TestCase
from settings import SERVER_URL

#class ApiTestCase(TestCase):  # should be object
class ApiTestCase(object):

    response = None
    server_url = SERVER_URL.rstrip('/')

    def request(self, method, uri, *args, **kwargs):
        if 'headers' in kwargs:
            headers = kwargs.pop('headers')
        else:
            headers = {}
        url = self.server_url + uri
        headers.update({'Authorization': self.token})
        self.response = self.session.request(
            method, url, *args,
            verify=False, headers=headers, **kwargs)

    def GET(self, *args, **kwargs):
        self.request('GET', *args, **kwargs)

    def POST(self, *args, **kwargs):
        self.request('POST', *args, **kwargs)

    def PATCH(self, *args, **kwargs):
        self.request('PATCH', *args, **kwargs)

    def PUT(self, *args, **kwargs):
        self.request('PUT', *args, **kwargs)

    def DELETE(self, *args, **kwargs):
        self.request('DELETE', *args, **kwargs)

    def expect_status(self, code):
        self.assertEqual(code, self.response.status_code,
                         "Status code not matches.")

    def expect_header(self, header, value):
        headers_low = {k.lower(): v.lower()
                       for k, v in self.response.headers.items()}
        self.assertIn(header.lower(), headers_low,
                      "No such header in response.")
        self.assertEqual(value.lower(), headers_low[header.lower()],
                         "Header not matches.")
