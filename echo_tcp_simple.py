#!/usr/bin/env python3
"""Simple TCP server"""
import socket

SERVER = "127.0.0.10"
PORT = 53

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connect by {addr}")
        while True:
            data = conn.recv(1024)  # How large can DNS requests be?
            if not data:
                break
            reply = bytes(data.decode('utf8').upper(),'utf8')
            conn.sendall(reply)
