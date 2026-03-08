class SotApi:
    def __init__(self, ipaddress, port):
        self.ipaddress = ipaddress
        self.port = port

    def send(self, obj:dict):
        print("data sent to SOT DB")