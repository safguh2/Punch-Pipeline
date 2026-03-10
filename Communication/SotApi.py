class SotApi:
    def __init__(self, ipaddress, port):
        self.ipaddress = ipaddress
        self.port = port

    def send(self, obj: list):
        print("data sent to SOT DB")
