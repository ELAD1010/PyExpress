import json

from httper.common.inet.helpers.flag_converter import FLAGS


class L4:
    def __init__(self, src_port, dst_port):
        self.src_port = src_port
        self.dst_port = dst_port


class TCP(L4):
    def __init__(self, src_port, dst_port, sequence, ack, header_len, flags, window, checksum, urgent_pointer):
        super().__init__(src_port, dst_port)
        self.sequence_number = sequence
        self.ack_number = ack
        self.header_length = header_len
        self.flags = flags
        self.window = window
        self.checksum = checksum
        self.urgent_pointer = urgent_pointer

    def __str__(self):
        return json.dumps({"sport": self.src_port, "dport": self.dst_port, "sequence_num": self.sequence_number, "ack_num": self.ack_number, "header_length": self.header_length, "flags": FLAGS[self.flags], "window": self.window, "checksum": self.checksum, "urgent_pointer": self.urgent_pointer})


class UDP(L4):
    def __init__(self, src_port, dst_port, length, checksum):
        super().__init__(src_port, dst_port)
        self.length = length
        self.checksum = checksum

    def __str__(self):
        return json.dumps({"sport": self.src_port, "dport": self.dst_port, "length": self.length, "checksum": self.checksum})
