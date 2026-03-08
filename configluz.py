from Neo4jApi import Neo4jApi
import json


def load_config():
    with open("configuration.json") as configuration_file:
        config = json.load(configuration_file)

        relation_label = config["relation_label"]

        api = Neo4jApi(config["api"]["ipaddress"], config["api"]["port"], relation_label)
        kafka_address = config["kafka"]["address"]
        rabbitmq_address = config["rabbitmq"]["address"]

        return api, kafka_address, rabbitmq_address
