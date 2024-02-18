import struct

class StructUtils:

    @staticmethod
    def unpack_ip_layer(ip_layer_bytes):
        return struct.unpack('!BBHHHBBHII', ip_layer_bytes)
    
    def unpack_transport_layer(transport_layer_bytes):
        return struct.unpack('!HHIIHHHH', transport_layer_bytes)
