import json
from requests import Session
from termcolor import colored
from pprint import pprint
from unittest import TestCase, TextTestResult, TextTestRunner

from api_test_tool.auth import log_in
from api_test_tool.settings import (
    SERVER_URL, PRINT_URL, XML_OUTPUT, VERBOSITY, PRINT_PAYLOAD)


class ApiTestResult(TextTestResult):

    def startTest(self, test):
        super(TextTestResult, self).startTest(test)
        if self.showAll:
            self.stream.writeln(colored('_' * 70, 'grey'))
            self.stream.writeln(
                colored(self.getDescription(test), 'magenta')
            )

    def addSuccess(self, test):
        super(TextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln(colored("ok", 'green'))
        elif self.dots:
            self.stream.write(colored('.', 'green'))
            self.stream.flush()

    def addError(self, test, err):
        super(TextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln(colored("ERROR", 'yellow'))
        elif self.dots:
            self.stream.write(colored('E', 'yellow'))
            self.stream.flush()

    def addFailure(self, test, err):
        super(TextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln(colored("FAIL", 'red'))
        elif self.dots:
            self.stream.write(colored('F', 'red'))
            self.stream.flush()


class ApiTestRunner(TextTestRunner):
    resultclass = ApiTestResult


class ApiTestCase(TestCase):

    def apply_path(self, json_dict, path):
        if path:
            path_elements = path.split('/')
            for element in path_elements:
                try:
                    json_dict = json_dict[element]
                except (IndexError, TypeError):
                    self.fail("Path can't be applied")
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

    maxDiff = None

    session = None
    token = None
    response = None
    server_url = SERVER_URL.rstrip('/')

    def request(self, method, uri, *args,
                add_server=True, with_auth=True, **kwargs):
        if not self.session:
            self.session = Session()

        if add_server:
            url = self.server_url + uri
        else:
            url = uri

        if 'headers' in kwargs:
            headers = kwargs.pop('headers')
        else:
            headers = {}
        if with_auth:
            if not self.token:
                self.token = log_in(session=self.session)
            headers.update({'Authorization': self.token})

        if VERBOSITY == 2:
            if PRINT_URL:
                print('{method} {url}'.format(method=method, url=url))
            if PRINT_PAYLOAD and 'data' in kwargs:
                pprint(kwargs['data'])
        self.response = self.session.request(
            method, url, *args,
            verify=False, headers=headers, **kwargs)

    def request_with_data(self, method,  uri, data='', *args, **kwargs):
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)
        self.request(method, uri, *args, data=data, **kwargs)

    def GET(self, *args, **kwargs):
        self.request('GET', *args, **kwargs)

    def POST(self, *args, **kwargs):
        self.request_with_data('POST', *args, **kwargs)

    def PATCH(self, *args, **kwargs):
        self.request_with_data('PATCH', *args, **kwargs)

    def PUT(self, *args, **kwargs):
        self.request_with_data('PUT', *args, **kwargs)

    def DELETE(self, *args, **kwargs):
        self.request('DELETE', *args, **kwargs)

    def expect_status(self, code):
        self.assertEqual(code, self.response.status_code,
                         "Status code not matches.")

    def expect_header(self, header, value, partly=False):
        self.assertIn(header, self.response.headers,
                      "No such header in response.")
        if partly:
            self.assertIn(value.lower(),
                          self.response.headers[header].lower(),
                          "Header not matches.")
        else:
            self.assertEqual(value.lower(),
                             self.response.headers[header].lower(),
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

    def expect_json_length(self, length, path=None):
        """
        checks if count of objects in json response equals provided length,
        path separated by slashes, ie 'foo/bar/spam'
        """
        json_response = self.apply_path(self.parse_json_response(), path)
        self.assertEqual(length, len(json_response),
                         "JSON objects count not matches.")

    def expect_body_contains(self, body):
        self.assertIn(body, self.response.text,
                      "Body not matches.")

    @property
    def json_response(self):
        json_dict = self.parse_json_response()
        return json_dict

    def inspect_json(self):
        pprint(self.json_response)

    def inspect_body(self):
        pprint(self.response.text)

    def inspect_status(self):
        print(self.response.status_code)

    def inspect_headers(self):
        pprint(dict(self.response.headers))
