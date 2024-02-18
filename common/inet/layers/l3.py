import json


class IP:
    def __init__(self, version, header_length, type_of_service, total_length, ttl, protocol, header_checksum, src_ip, dst_ip):
        self.version = version 
        self.header_length = header_length
        self.type_of_service =  type_of_service
        self.total_length = total_length
        self.ttl = ttl
        self.protocol = protocol
        self.header_checksum = header_checksum
        self.src_ip = src_ip
        self.dst_ip = dst_ip

    def __str__(self):
        return json.dumps({'version': self.version, 'header_length': self.header_length, 'ttl': self.ttl,
              'protocol': self.protocol, 'checksum': self.header_checksum, 'src_ip': self.src_ip, 'dst_ip': self.dst_ip, 'total_length': self.total_length})
