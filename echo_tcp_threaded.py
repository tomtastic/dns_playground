#!/usr/bin/env python3
"""Threaded TCP server"""
import socketserver
import threading


class EchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print(f"connect from {self.client_address}")
        data = self.request.recv(1024)
        # Just echo the request back in upper case
        reply = bytes(data.decode("utf8").upper(), "utf8")
        self.request.send(reply)
        return


if __name__ == "__main__":
    SERVER = "127.0.0.10"
    PORT = 53

    server = socketserver.TCPServer((SERVER, PORT), EchoRequestHandler)
    print(f"Server bind on : {server.server_address}")

    t = threading.Thread(target=server.serve_forever)
    t.daemon = False
    t.start()
