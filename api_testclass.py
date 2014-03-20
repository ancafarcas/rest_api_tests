import json
from requests import Session
from unittest import TestCase

from settings import SERVER_URL


class Helpers():

    def apply_path(self, json_dict, path):
        if path:
            path_elements = path.split('/')
            for element in path_elements:
                json_dict = json_dict[element]
        return json_dict

    def parse_json_input(self, json_dict):
        if isinstance(json_dict, str) \
           and ('{' in json_dict or '[' in json_dict):
            try:
                response_dict = json.loads(self.response.text)
            except ValueError:
                self.fail('You have provided not a valid JSON.')
        return json_dict

    def parse_json_response(self):
        try:
            response_dict = json.loads(self.response.text)
        except ValueError:
            self.fail('Response in not a valid JSON.')
        return response_dict


#class ApiTestCase(TestCase, Helpers):  # should be object; this line for cmplt
class ApiTestCase(Helpers):

    session = None
    token = None
    response = None
    server_url = SERVER_URL.rstrip('/')

    def request(self, method, uri, *args, add_server=True, **kwargs):
        if not self.session:
            self.session = Session()

        if add_server:
            url = self.server_url + uri
        else:
            url = uri

        if self.token:
            if 'headers' in kwargs:
                headers = kwargs.pop('headers')
            else:
                headers = {}
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

    def expect_header(self, header, value, partly=False):
        headers_low = {k.lower(): v.lower()
                       for k, v in self.response.headers.items()}
        self.assertIn(header.lower(), headers_low,
                      "No such header in response.")
        if partly:
            self.assertIn(value.lower(), headers_low[header.lower()],
                          "Header not matches.")
        else:
            self.assertEqual(value.lower(), headers_low[header.lower()],
                             "Header not matches.")

    def expect_header_contains(self, header, value):
        self.expect_header(header, value, partly=True)

    def expect_json(self, json_input, path=None, partly=False):
        """
        checks if json response equals some json,
        path separated by slashes, ie 'foo/bar/spam'
        """
        json_input = self.parse_json_input(json_input)
        json_response = self.apply_path(self.parse_json_response(), path)

        if partly:
            if isinstance(json_input, dict):
                self.assertDictContainsSubset(
                    json_input, json_response, "JSON not matches")
            elif isinstance(json_input, list):
                self.assertIn(
                    json_input, json_response, "JSON not matches")
        else:
            if isinstance(json_input, dict):
                self.assertDictEqual(
                    json_input, json_response, "JSON not matches")
            elif isinstance(json_input, list):
                self.assertEqual(
                    json_input, json_response, "JSON not matches")

        if isinstance(json_input, str):
            self.assertEqual(
                json_input, json_response, "JSON not matches")

    def expect_json_contains(self, json_input, path=None):
        """
        checks if json response contains some json subset,
        path separated by slashes, ie 'foo/bar/spam'
        """
        self.expect_json(json_input, path, partly=True)
