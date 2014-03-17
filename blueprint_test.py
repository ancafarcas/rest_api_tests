import unittest
import json

from pprint import pprint

with open('./apiary.json', 'r') as f:
    json_blueprint = json.loads(f.read())


class meta_BlueprintTest(type):

    @classmethod
    def __prepare__(mcls, name, bases):
        testset = [
            (r["name"], r["resources"]) for r in
                [g for g in json_blueprint["resourceGroups"]]
        ]
        d = dict()
        d['testme'] = 5
        for resource_name, resource in testset:
            for action in resource:
                name = action['name']
                fname = "test {resource} -> {action}".format(
                    resource=resource_name, action=name)
                d[fname] = mcls.build_test(action)
        return d

    @classmethod
    def build_test(cls, action):
        def f(self):
            uri = action['uriTemplate']
            print(uri)
        return f

class BlueprintTestCase(unittest.TestCase, metaclass=meta_BlueprintTest):
    pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
