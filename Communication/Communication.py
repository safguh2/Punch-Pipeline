from Communication.SotApi import SotApi
from Communication.Neo4jApi import Neo4jApi
from Communication.DataPasrer import parse_data
from Communication.SchemaParser import parse_schema
import Communication.SotProtocol as SotProtocol

class Communication:
    def __init__(self, neo: Neo4jApi, sot: SotApi):
        self.neo: Neo4jApi = neo
        self.sot: SotApi = sot

    def send(self, obj: dict):
        self.neo.send(obj)
        self.sot.send(obj)

    def update_sot(self):
        data = self.neo.get_data()
        schemas = self.neo.get_schemas()

        entities, relations = parse_data(data)
        label_schemas, relation_schemas = parse_schema(schemas)

        entity_requests = SotProtocol.parse_entity_request(entities)
        schemas_requests = SotProtocol.parse_label_schema_request(label_schemas)


