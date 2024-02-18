import threading
import socket

from lib.parser import PduParser
from common.inet.enums.pdu_type import PduType
from common.inet.helpers.flag_converter import Flags

from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTP
from scapy.layers.inet import TCP, IP


MTU = 65535


class HttpSniffer(socket.socket, threading.Thread):
    def __init__(self, ip, port, responder):
        threading.Thread.__init__(self)
        super().__init__(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.parser = PduParser()
        self.ip = ip
        self.port = port
        self.responder = responder
        self.bind(("0.0.0.0", self.port))

    def __send_syn_ack_packet(self, pdu):
        pdu.transport.flags = Flags.SYN_ACK # Set flags to syn-ack

        pdu.transport.src_port, pdu.transport.dst_port = pdu.transport. dst_port, pdu.transport.src_port # Switch ports
        pdu.ip.src_ip, pdu.ip.dst_ip = pdu.ip.dst_ip, pdu.ip.src_ip

        pdu.transport.ack_number = pdu.transport.sequence_number + 1

        pdu_to_send = IP(src=pdu.ip.src_ip, dst=pdu.ip.dst_ip) / TCP(
            sport=pdu.transport.src_port, dport=pdu.transport.dst_port, flags='SA',
            ack=pdu.transport.ack_number)

        ack_packet = sr1(pdu_to_send, verbose=0)
        if ack_packet[TCP].flags != 'A':
            # Todo: Retransmit syn_ack
            pass

    def __send_rst_packet(self, pdu):

        pdu.transport.src_port, pdu.transport.dst_port = pdu.transport.dst_port, pdu.transport.src_port  # Switch ports
        pdu.transport.ack_number = pdu.transport.sequence_number + 1
        pdu.transport.sequence_number = 1

        pdu.ip.src_ip, pdu.ip.dst_ip = pdu.ip.dst_ip, pdu.ip.src_ip

        rst_packet = IP(src=pdu.ip.src_ip, dst=pdu.ip.dst_ip) / TCP(sport=pdu.transport.src_port,
                                                                            dport=pdu.transport.dst_port, flags="RA",
                                                                            seq=pdu.transport.sequence_number,
                                                                            ack=pdu.transport.ack_number)
        send(rst_packet, verbose=0)

    def run(self):
        print(f'Listening on port {self.port}')
        while True:
            pdu, address = self.recvfrom(MTU)
            pdu, pdu_type = self.parser.parse_pdu(pdu)

            if pdu_type is None:
                continue

            if pdu.transport.dst_port != self.port:
                self.__send_rst_packet(pdu)

            elif pdu_type == PduType.SynSegment:
                self.__send_syn_ack_packet(pdu)

            elif pdu_type == PduType.HttpRequest:
                self.responder.append_request(pdu)






