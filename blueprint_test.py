import unittest
import json
import requests

from pprint import pprint


SERVER_URL = 'http://superdesk.apiary.io'


with open('./apiary.json', 'r') as f:
    json_blueprint = json.loads(f.read())


class meta_BlueprintTest(type):

    @classmethod
    def __prepare__(mcls, name, bases):
        tests_dict = dict()
        for resource_group in json_blueprint["resourceGroups"]:
            for resource in resource_group["resources"]:
                for action in resource["actions"]:
                    for example in action["examples"]:
                        fname = "test {resource_group} > {resource} > {action} > {example}".format(
                            resource_group=resource_group["name"],
                            resource=resource["name"],
                            action=action["name"],
                            example=example["name"]
                        )
                        tests_dict[fname] = mcls.build_test(
                            resource, action, example)
        return tests_dict

    @classmethod
    def build_test(cls, resource, action, example):
        def func(self):
            print()
            # model
            #try:
            #    model = json.loads(resource['model']['body'])
            #except (ValueError, KeyError):
            #    model = {}

            # request
            try:
                if len(example['requests']) > 1:
                    print('warn: Multiple requests, using first')
                payload = json.loads(example['requests'][0]['body'])
            except (ValueError, IndexError):
                payload = {}
            # response
            code = json.loads(example['responses'][0]['name'])
            try:
                if len(example['responses']) > 1:
                    print('warn: Multiple responses, using first')
                answer = json.loads(example['responses'][0]['body'])
            except ValueError:
                answer = None
            # endpoint
            method = action["method"]
            if len(resource['parameters']) > 0:
                parameters = {p['name']: p['example']
                              for p in resource['parameters']}
                uri = resource['uriTemplate'].format(**parameters)
            else:
                uri = resource['uriTemplate']
            url = SERVER_URL + uri
            # executing
            print(url)
            response = self.session.request(method, url,
                                            data=json.dumps(payload))
            self.assertEqual(code, response.status_code)
            if answer:
                self.assertEqual(answer, json.loads(response.text))

        return func


class BlueprintTestCase(unittest.TestCase, metaclass=meta_BlueprintTest):

    @classmethod
    def setUpClass(cls):
        #auth will be here
        cls.session = requests.Session()

if __name__ == '__main__':
    unittest.main(verbosity=2)
