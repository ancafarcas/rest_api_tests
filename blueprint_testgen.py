import json

from settings import (
    SERVER_URL, BLUEPRINT_URL, BLUEPRINT_PATH, IGNORE_ENDPOINTS)


with open(BLUEPRINT_PATH, 'r') as f:
    json_blueprint = json.loads(f.read().replace(BLUEPRINT_URL, SERVER_URL))

name_template = "test {resource_group} > {resource} > {action} > {example}"


class meta_BlueprintTest(type):

    server_url = SERVER_URL.rstrip('/')

    @classmethod
    def __prepare__(mcls, name, bases):
        tests_dict = dict()
        for resource_group in json_blueprint["resourceGroups"]:
            for resource in resource_group["resources"]:
                for action in resource["actions"]:
                    for example in action["examples"]:
                        fname = name_template.format(
                            resource_group=resource_group["name"],
                            resource=resource["name"],
                            action=action["name"],
                            example=example["name"]
                        )
                        if resource['uriTemplate'] not in IGNORE_ENDPOINTS:
                            tests_dict[fname] = mcls.build_test(
                                resource, action, example)
        return tests_dict

    @classmethod
    def prepare_request(cls, example):
        try:
            if len(example['requests']) > 1:
                print('warn: Multiple requests, using first')
            payload = json.loads(example['requests'][0]['body'])
        except (ValueError, IndexError):
            payload = {}
        return payload

    @classmethod
    def prepare_response(cls, example):
        if len(example['responses']) > 1:
            print('warn: Multiple responses, using first')
        code = json.loads(example['responses'][0]['name'])
        try:
            answer = json.loads(example['responses'][0]['body'])
        except ValueError:
            answer = None
        headers = {h['name']: h['value']
                   for h in example['responses'][0]['headers']}
        return code, answer, headers

    @classmethod
    def prepare_endpoint(cls, resource, action):
        # @TODO: add substitution for GET parameters
        method = action['method']
        if len(resource['parameters']) > 0:
            parameters = {p['name']: p['example']
                          for p in resource['parameters']}
            uri = resource['uriTemplate'].format(**parameters)
        else:
            uri = resource['uriTemplate']
        url = cls.server_url + uri
        return method, url

    @classmethod
    def build_test(cls, resource, action, example):
        def func(self):
            print()
            payload = cls.prepare_request(example)
            code, answer, headers = cls.prepare_response(example)
            method, url = cls.prepare_endpoint(resource, action)
            print(url)
            self.request(
                method, url, data=json.dumps(payload))
            self.expect_status(code)
            for header, value in headers.items():
                self.expect_header(header, value)
            if answer:
                self.assertEqual(answer, json.loads(self.response.text))

        return func
