import socket
import struct

class ByteUtils:
    
    @staticmethod
    def parse_byte_to_4_bits_tuple(byte_to_parse: int):
        if byte_to_parse < 0 or byte_to_parse > 255:
            print("number is not a byte size")

        left_4_bit = (byte_to_parse >> 4) & 0x0F
        right_4_bit = byte_to_parse & 0x0F

        return left_4_bit, right_4_bit
    
    def parse_bytes_to_ip_address(bytes_to_parse: int):
        return socket.inet_ntoa(struct.pack(">L", bytes_to_parse))
    