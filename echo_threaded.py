#!/usr/bin/env python3
"""Threaded TCP and UDP server"""
"""eg."""
"""echo "hello" | socat - TCP4:127.0.0.10:53"""
"""echo "hello" | socat - UDP4:127.0.0.10:53"""

import socketserver
import threading


class TCPEchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        """Just echo back in upper case"""
        print(f"connection(TCP) from {self.client_address[0]}:{self.client_address[1]}")
        data = self.request.recv(1024)
        self.request.send(b"TCP:" + data.upper())


class UDPEchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        """Just echo back in upper case"""
        print(f"connection(UDP) from {self.client_address[0]}:{self.client_address[1]}")
        data = self.request[0]
        socket = self.request[1]
        socket.sendto(b"UDP:" + data.upper(), self.client_address)


if __name__ == "__main__":
    SERVER, PORT = "127.0.0.10", 53

    try:
        server_tcp = socketserver.TCPServer((SERVER, PORT), TCPEchoRequestHandler)
        t_tcp = threading.Thread(target=server_tcp.serve_forever)
        t_tcp.daemon = False
        t_tcp.start()
        print(f"Thread {t_tcp.native_id} listening on TCP : {server_tcp.server_address}")
    except:
        raise

    try:
        server_udp = socketserver.UDPServer((SERVER, PORT), UDPEchoRequestHandler)
        t_udp = threading.Thread(target=server_udp.serve_forever)
        t_udp.daemon = False
        t_udp.start()
        print(f"Thread {t_udp.native_id} listening on UDP : {server_udp.server_address}")
    except:
        raise
