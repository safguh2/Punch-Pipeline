from Neo4jApi import Neo4jApi
from SotApi import SotApi
from Communication import Communication
import json


def load_config():
    with open("configuration.json") as configuration_file:
        config = json.load(configuration_file)

        relation_label = config["relation_label"]

        neo_api = Neo4jApi(config["api"]["ipaddress"], config["api"]["port"], relation_label)
        sot_api = SotApi(config['sot']['ipaddress'], config['sot']['port'])
        communicator = Communication(neo_api, sot_api)

        kafka_address = config["kafka"]["address"]
        rabbitmq_address = config["rabbitmq"]["address"]

        workers_amount = config["worker_amount"]

        return communicator, kafka_address, rabbitmq_address, workers_amount
