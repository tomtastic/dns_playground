#!/usr/bin/env python3
"""
    Threaded TCP and UDP server
    eg. UDP query
    $ dig +notcp +retry=0 @127.0.0.10 example.com TXT
    eg. TCP query
    $ dig   +tcp +retry=0 @127.0.0.10 example.com TXT
"""

import socketserver
import threading
import dns.message
import dns.query
import dns.name
import dns.rrset
import dns.rdataclass
import dns.rdatatype
import dns.flags
import dns.resolver


class TCPDNSRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        """Respond with fixed answer"""
        ip, port = self.client_address
        data = self.request.recv(4096)
        try:
            # TODO dns.query.receive_tcp ?
            message = dns.message.from_wire(wire=data[2:])  # Strip 2 bytes of TCP?
            message_question = message.question.pop()
            print(f"{ip}:{port} [TCP] {message_question}")
            query_name = str(message_question).split(' ')[0]
            response = dns.message.make_response(message)
            #response.flags |= dns.flags.AA
            txt = dns.rrset.from_text_list(
                name=query_name,
                ttl=300,
                rdclass=dns.rdataclass.IN,
                rdtype=dns.rdatatype.TXT,
                text_rdatas=["fake=123txt"],
            )
            response.answer.append(txt)
            dns.query.send_tcp(self.request,response)
        except Exception as e:
            print(f"{ip}:{port} [TCP] Not parsable as DNS message : {e}")


class UDPDNSRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        """Respond with fixed answer"""
        ip, port = self.client_address
        data = self.request[0]
        socket = self.request[1]
        try:
            message = dns.message.from_wire(wire=data)
            message_question = message.question.pop()
            print(f"{ip}:{port} [UDP] {message_question}")
            query_name = str(message_question).split(' ')[0]
            response = dns.message.make_response(message)
            #response.flags |= dns.flags.AA
            txt = dns.rrset.from_text_list(
                name=query_name,
                ttl=300,
                rdclass=dns.rdataclass.IN,
                rdtype=dns.rdatatype.TXT,
                text_rdatas=["fake=123txt"],
            )
            response.answer.append(txt)
            dns.query.send_udp(socket,response,destination=self.client_address)
        except Exception as e:
            print(f"{ip}:{port} [UDP] Not parsable as DNS message : {e}")


if __name__ == "__main__":
    SERVER, PORT = "127.0.0.10", 53

    try:
        server_tcp = socketserver.TCPServer((SERVER, PORT), TCPDNSRequestHandler)
        t_tcp = threading.Thread(target=server_tcp.serve_forever)
        t_tcp.daemon = False  # Dont exit
        t_tcp.start()
        print( f"Thread {t_tcp.native_id} listening TCP : {server_tcp.server_address}")
    except Exception as e:
        print(f"Caught : {e}")
        raise

    try:
        server_udp = socketserver.UDPServer((SERVER, PORT), UDPDNSRequestHandler)
        t_udp = threading.Thread(target=server_udp.serve_forever)
        t_udp.daemon = False  # Dont exit
        t_udp.start()
        print( f"Thread {t_udp.native_id} listening UDP : {server_udp.server_address}")
    except Exception as e:
        print(f"Caught : {e}")
        raise
