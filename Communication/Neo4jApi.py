import ast
import json
import requests
from Communication.SchemaParser import parse_response


class Neo4jApi:
    def __init__(self, url: str, relation_schema: dict):
        self.url = url
        self.relation_schema = relation_schema

    def send(self, obj: dict):
        if obj['label'] == self.relation_schema["label"]:
            # res = requests.post(f'{self.url}/relationships', json=obj["properties"])
            print(f'relation has been sent to neo4j DB {str(obj)}')

        else:
            # res = requests.post(f'{self.url}/dynamic/smart-create', data=str(obj))
            print(f'object has been sent to neo4j DB {str(obj)}')


    def get_schemas(self):
        response = requests.get(f'{self.url}/schema').text
        raw = json.loads(response)
        raw["nodeLabels"].append(self.relation_schema)
        return raw

    def get_data(self):
        response = requests.get(f'{self.url}/data/all').text
        return json.loads(response)
