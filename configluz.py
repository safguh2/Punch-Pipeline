from api import Api
import json

def loadConfig():
    with open("configuration.json") as configuration_file:
        config = json.load(configuration_file)

        api = Api(config["api"]["ipaddress"], config["api"]["port"])
        kafka_address = config["kafka"]["address"]

        return api, kafka_address