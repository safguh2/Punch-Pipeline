import ast
import json
import requests


class Neo4jApi:
    def __init__(self, url: str, relation_schema: dict):
        self.url = url
        self.relation_schema = relation_schema

    def send(self, obj: dict):
        if obj['label'] == self.relation_schema["label"]:
            res = requests.post(f'{self.url}/relationships', json=obj["properties"])
            print(f'relation has been sent to neo4j DB {str(obj)}')

        else:
            res = requests.post(f'{self.url}/dynamic/smart-create', data=str(obj))
            print(f'object has been sent to neo4j DB {str(obj)}')


    def get_schemas(self):
        #response = requests.get(f'{self.url}/schema').text
        response = get_mock_data()
        raw = json.loads(response)
        raw["nodeLabels"].append(self.relation_schema)
        return parse_response(raw["nodeLabels"])


api_type_dictionary = {"string": str, "integer": int, "float": int, "boolean": bool, "date": str, "dict": dict}


def parse_response(response):
    schemas = list()
    print(response)
    for schema in response:
        label = schema['label']

        fields = parse_fields(schema['properties'])

        schemas.append({"label": label, "properties": fields})

    return schemas


def parse_fields(raw_fields):
    fields = dict()
    print(raw_fields)
    for field in raw_fields:
        type = api_type_dictionary[field["type"].lower()]
        fields[field['name']] = (type, ...)

    return fields


def get_mock_data():
    with open("../mock_data.json") as data:
        binary = data.read()
        return binary
