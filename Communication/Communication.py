from Communication.SotApi import SotApi
from Communication.Neo4jApi import Neo4jApi
from Communication.DataPasrer import parse_data


class Communication:
    def __init__(self, neo: Neo4jApi, sot: SotApi):
        self.neo: Neo4jApi = neo
        self.sot: SotApi = sot

    def send(self, obj: dict):
        self.neo.send(obj)
        self.sot.send(obj)

    def update_sot(self):
        data = self.neo