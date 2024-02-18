class Pdu:
    def __init__(self, ip_layer, transport_layer, raw=None):
        self.ip = ip_layer
        self.transport = transport_layer
        self.raw = raw
