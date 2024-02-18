import json

from httper.inet.enums.Ip import IpHeaders
from httper.inet.enums.L4Protocol import L4Protocol
from httper.inet.enums.Tcp import TcpHeaders
from httper.inet.enums.Udp import UdpHeaders
from httper.inet.helpers.flag_converter import FLAGS
from httper.inet.layers.l3 import IP
from httper.inet.layers.l4 import TCP, UDP
from httper.inet.layers.l7 import HTTP
from httper.inet.layers.layers import Layers


class Packet:
    def __init__(self, ip_header, l4_header, raw_data):
        self.headers = self.__build(ip_header, l4_header, raw_data)

    def __build(self, ip_header, l4_header, raw_data):
        ip_layer = Packet.__build_ip_layer(ip_header)
        l4 = Packet.__build_l4_layer(l4_header)
        raw_data = Packet.__build_raw_data(raw_data, l4)
        return {"IP": ip_layer, "L4": l4, "RAW": raw_data}

    def has_layer(self, layer: Layers):
        for header in self.headers.values():
            if type(header) is layer:
                return True
        return False

    def __str__(self):
        return "{\r\n"\
               f"IP: {self.headers['IP']}\r\n" \
               f"L4: {self.headers['L4']}\r\n" \
               f"RAW: {self.headers['RAW']}"\
               "\r\n}"

    @staticmethod
    def __build_ip_layer(ip_header):
        src_ip = IP.parse_ip_address(ip_header[IpHeaders.SrcIp: IpHeaders.DstIp])
        dst_ip = IP.parse_ip_address(ip_header[IpHeaders.DstIp:])
        ttl = ip_header[IpHeaders.TTL]
        protocol = ip_header[IpHeaders.Protocol]
        return IP(src_ip, dst_ip, ttl, protocol)

    @staticmethod
    def __build_l4_layer(l4_header_info):
        l4_header = l4_header_info['data']
        if l4_header_info['protocol'] == L4Protocol.TCP:
            src_port = l4_header[TcpHeaders.SrcPort]
            dst_port = l4_header[TcpHeaders.DstPort]
            sequence = l4_header[TcpHeaders.SequenceNumber]
            ack = l4_header[TcpHeaders.Ack]
            flags = l4_header[TcpHeaders.Flag]
            data_offset = (l4_header[TcpHeaders.DataOffset] >> 4) * 4
            return TCP(src_port, dst_port, sequence, ack, flags, data_offset)
        if l4_header_info['protocol'] == L4Protocol.UDP:
            src_port = l4_header[UdpHeaders.SrcPort]
            dst_port = l4_header[UdpHeaders.DstPort]
            length = l4_header[UdpHeaders.Length]
            checksum = l4_header[UdpHeaders.Checksum]
            return UDP(src_port, dst_port, length, checksum)

    @staticmethod
    def __build_raw_data(raw_packet, l4_layer):
        if type(l4_layer) is TCP:
            data_offset = l4_layer.data_offset
        else:
            data_offset = l4_layer.length
        raw_data = raw_packet[20 + data_offset:]
        if not raw_data:
            return None
        data = raw_data.decode().split('\r\n')
        if 'HTTP' in data[0]:
            return HTTP(data)






