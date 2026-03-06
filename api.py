import ast

import requests


class Api:
    def __init__(self, ipaddress, port):
        self.url = f"http://{ipaddress}:{str(port)}/api"
        self.index = 0

    def send(self, obj:dict):
        print(f'object has been sent: {str(obj)}')

    def get_schemas(self):
        #response = requests.get(f'{self.url}/schema')
        response = get_mock_data()
        # digest the response
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
