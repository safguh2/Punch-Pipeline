from Communication.Neo4jApi import Neo4jApi
from Communication.SotApi import SotApi
from Communication.Communication import Communication
import json


def load_config():
    with open("configuration.json") as configuration_file:
        config = json.load(configuration_file)

        relation_schema = config["relation_schema"]

        neo_api = Neo4jApi(config["api"]["url"], relation_schema)
        sot_api = SotApi(config['sot']['ipaddress'], config['sot']['port'])
        communicator = Communication(neo_api, sot_api)

        kafka_address = config["kafka"]["address"]
        rabbitmq_address = config["rabbitmq"]["address"]

        workers_amount = config["worker_amount"]

        external_dbs = config["external_db"]

        return communicator, kafka_address, rabbitmq_address, workers_amount, external_dbs
