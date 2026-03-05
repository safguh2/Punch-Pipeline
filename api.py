import requests


class Api:
    def __init__(self, ipaddress, port):
        self.url = f"http://{ipaddress}:{str(port)}/api"
        self.index = 0

    def send(self, obj:dict):
        print(f'object has been sent: {str(obj)}')

    def get_schemas(self):
        #response = requests.get(f'{self.url}/schema')
        # digest the response
        first_schema = [{'label': "test", 'fields': {"test": (int, ...)}}]
        second_schema = [{'label': "test", 'fields': {"test": (str, ...)}}]
        self.index += 1

        if(self.index%2==0):
            return first_schema
        else:
            return second_schema