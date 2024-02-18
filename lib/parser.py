from utils.struct_utils import StructUtils
from utils.byte_utils import ByteUtils

from common.inet.layers.l3 import IP
from common.inet.layers.l4 import TCP

from common.inet.helpers.flag_converter import Flags
from common.inet.enums.L4Protocol import L4Protocol
from common.inet.enums.pdu_type import PduType
from common.inet.pdu import Pdu

from httper.common.inet.layers.l7 import HTTP


class PduParser:

    def parse_ip_layer(self, pdu):
        '''
        version + header length = [:1]
        type of service = [1:2]
        total length = [2:4]
        identification = [4:6]
        flags + fragmentOffest = [6:8]
        time to live = [8:9]
        protocol = [9:10]
        header checksum = [10:12]
        srcIp = [12:16]
        destIp = [16:20]
        '''
          
        unpacked_pdu = StructUtils.unpack_ip_layer(pdu[0:20])
        version_header_length, type_of_service, total_length, identification, flags_frag_offset, ttl, protocol, header_checksum, src_ip_decimal, dst_ip_decimal = unpacked_pdu
        ip_version, header_length = ByteUtils.parse_byte_to_4_bits_tuple(version_header_length)

        src_ip = ByteUtils.parse_bytes_to_ip_address(src_ip_decimal)
        dst_ip = ByteUtils.parse_bytes_to_ip_address(dst_ip_decimal)

        return IP(ip_version, header_length, type_of_service, total_length, ttl,
                     protocol, header_checksum, src_ip, dst_ip)
    
    def parse_transport_layer(self, pdu):
        '''
            source port = [0] (16 bits) (H)
            destination port = [1] (16 bits) (H)
            sequence number = [2] (32 bits) (I)
            ack number = [3] (32 bits) (I)
            data offset = [4] (left) (4 bits) (H) oooo rrrr rrff ffff
            reserved (6 bits)
            flags (6 bits)
            window = [5] (16 bits) (H)
            checksum = [6] (16 bits) (H)
            urgent pointer = [7] (16 bits) (H)
        '''
        unpacked_pdu = StructUtils.unpack_transport_layer(pdu[20:40])
        src_port, dst_port, sequence_number, ack_number, header_length_flags, window, checksum, urgent_pointer = unpacked_pdu

        header_length = (header_length_flags >> 12) * 4
        flags = header_length_flags & 0b0000000000111111

        return TCP(src_port, dst_port, sequence_number, ack_number, header_length, flags, window, checksum,
                   urgent_pointer)


    def parse_raw_data(self, raw_data):
        if not raw_data:
            return

        try:
            data = raw_data.decode().split('\r\n')
            if 'HTTP' in data[0]:
                return HTTP(data)
        except:
            return None
        return None #Ignore the raw_data if it is not http
    
    def parse_pdu(self, pdu):
        ip_layer = self.parse_ip_layer(pdu)

        if ip_layer.protocol != L4Protocol.TCP:
            return None, None

        # We parse only TCP which is the underlying protocol of http
        transport_layer = self.parse_transport_layer(pdu)

        if transport_layer.flags == Flags.SYN:
            return Pdu(ip_layer, transport_layer), PduType.SynSegment

        raw_data = self.parse_raw_data(pdu[20 + transport_layer.header_length:])

        if raw_data:
            return Pdu(ip_layer, transport_layer, raw_data), PduType.HttpRequest

        return Pdu(ip_layer, transport_layer), None
