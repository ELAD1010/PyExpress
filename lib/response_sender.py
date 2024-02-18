import json
import threading

from scapy.all import send
from scapy.layers.inet import IP, TCP

from httper.common.http_request import Request
from httper.common.http_response import Response
from httper.common.inet.layers.l7 import HTTP
from httper.common.inet.pdu import Pdu
from httper.errors.http_internal_server_error import HttpInternalServerError
from httper.errors.http_not_found_error import HttpNotFoundError


class ResponseSender(threading.Thread):

    def __init__(self, routes):
        self.buffered_http_requests: list[Pdu] = []
        self.routes = routes
        super().__init__(target=self.handle_http_requests)

    def append_request(self, request: Pdu):
        self.buffered_http_requests.append(request)

    def __build_http_response(self, protocol, status, err_msg, content_type, content):
        http_content = '\r\n'.join([f"{protocol} {status} {err_msg}", f"Content-Type: {content_type}",
                                    f"Content-Length:{len(content.encode('utf-8'))}", ""])
        http_content += "\r\n"
        http_content += content
        return http_content

    def respond(self, http_pdu: Pdu, protocol, content, status_code, err_msg="", content_type='application/json'):
        ip = IP(src=http_pdu.ip.dst_ip, dst=http_pdu.ip.src_ip)
        tcp_ack = TCP(sport=http_pdu.transport.dst_port, dport=http_pdu.transport.src_port, flags="A",
                      seq=http_pdu.transport.ack_number, ack=http_pdu.transport.sequence_number + http_pdu.raw.len)

        send(ip / tcp_ack, verbose=0)

        tcp_http_response_layer = TCP(sport=http_pdu.transport.dst_port, dport=http_pdu.transport.src_port,
                           flags="PA", seq=http_pdu.transport.ack_number, ack=http_pdu.transport.sequence_number + http_pdu.raw.len)

        http = self.__build_http_response(protocol, status_code, err_msg, content_type, str(content))

        http_response_packet = ip / tcp_http_response_layer / http

        send(http_response_packet, verbose=0)


    def handle_http_requests(self):
        while True:
            if len(self.buffered_http_requests) == 0:
                continue

            http_pdu = self.buffered_http_requests.pop(0)

            http_raw: HTTP = http_pdu.raw
            path_only = http_raw.path[0: http_raw.path.find('?')] if '?' in http_raw.path else http_raw.path
            if path_only in self.routes[http_raw.method]:
                http_request = Request(http_raw)
                handler = self.routes[http_request.method][http_request.path]['handler']
                success_status = self.routes[http_request.method][http_request.path]['status']
                try:
                    http_response = Response(success_status)
                    handler(http_request, http_response)  # Can throw an exception
                    data, status_code = http_response.data, http_response.status_code
                    self.respond(http_pdu, http_request.protocol, data, status_code)
                except (HttpInternalServerError, HttpNotFoundError) as err:
                    self.respond(http_pdu, http_request.protocol, json.dumps(
                        {'error': err.message, 'status': err.status}), err.status)
                except Exception as ex:
                    print(ex)
                    self.respond(http_pdu, http_request.protocol, json.dumps({'error': "Internal Server Error", 'status': 500}), 500)

            self.respond(http_pdu, http_raw.protocol, "Invalid path", 404, "Error", 'text/html')



