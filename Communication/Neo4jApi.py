import ast
import json
import requests


class Neo4jApi:
    def __init__(self, url: str, relation_schema: dict):
        self.url = url
        self.relation_schema = relation_schema
        self.headers = {
            "x-authz-user-id": "014d58c0-e788-4e53-bfa3-7986f242e7e1",
            "x-authz-username": "testing@example.com",
            "x-authz-read": "true",
            "x-authz-write": "true",
            "x-authz-is-admin": "true",
            "x-authz-env-level": "6",
        }

    def send(self, obj: dict):
        print(obj)
        if obj['label'] == self.relation_schema["label"]:
            # res = requests.post(f'{self.url}/relationships', json=obj["properties"], headers=self.headers)
            print(f'relation has been sent to neo4j DB {str(obj)}')

        else:
            # res = requests.post(f'{self.url}/dynamic/smart-create', json=str(obj), headers=self.headers)
            print(f'object has been sent to neo4j DB {str(obj)}')


    def get_schemas(self):
        response = requests.get(f'{self.url}/schema', headers=self.headers).text
        raw = json.loads(response)
        raw["nodeLabels"].append(self.relation_schema)
        return raw

    def get_data(self):
        response = requests.get(f'{self.url}/data/all', headers=self.headers).text
        return json.loads(response)
