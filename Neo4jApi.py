import ast

import requests


class Neo4jApi:
    def __init__(self, ipaddress: str, port: int, relation_label: str):
        self.url = f"http://{ipaddress}:{str(port)}/api"
        self.relation_label = relation_label

    def send(self, obj: dict):
        if obj['label'] == self.relation_label:
            print(f'relation has been sent to neo4j DB {str(obj)}')
        else:
            print(f'object has been sent to neo4j DB {str(obj)}')

    def get_schemas(self):
        # response = requests.get(f'{self.url}/schema')
        response = get_mock_data()
        return parse_response(response)


api_type_dictionary = {"STRING": str, "INTEGER": int, "FLOAT": int, "BOOLEAN": bool}


def parse_response(response):
    raw = ast.literal_eval(response.decode('utf-8'))['nodeLabels']
    schemas = list()

    for schema in raw:
        label = schema['label']

        fields = parse_fields(schema['properties'])

        schemas.append({"label": label, "fields": fields})

    return schemas


def parse_fields(raw_fields):
    fields = dict()

    for field in raw_fields:
        type = api_type_dictionary[field["type"]]
        fields[field['name']] = (type, ...)

    return fields


def get_mock_data():
    with open("mock_data.json") as data:
        binary = data.read()
        return binary.encode()
