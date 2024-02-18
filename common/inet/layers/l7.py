import json


class HTTP:
    def __init__(self, data):
        request = data[0].split(' ')
        self.method = request[0]
        self.path = request[1]
        self.protocol = request[2]
        self.len = len('\r\n'.join(data))
        self.body = {}
        if data[-1] != "":
            self.body = json.loads(data[-1])

    def __str__(self):
        return json.dumps({"method": self.method, "path": self.path, "protocol": self.protocol, "len": self.len, "body": self.body})
