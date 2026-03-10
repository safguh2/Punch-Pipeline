import Neo4jApi
import SotApi


class Communication:
    def __init__(self, neo: Neo4jApi, sot: SotApi):
        self.neo: Neo4jApi = neo
        self.sot: SotApi = sot

    def send(self, obj: dict):
        self.neo.send(obj)
        self.sot.send(obj)
