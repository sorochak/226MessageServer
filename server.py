#!/usr/bin/python3

import socket
import sys

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen(1) # Enable server to receive 1 connection at a time
print('Server: ', sock.getsockname()) # Source IP and port

while True:
    sc, sockname = sock.accept() # Wait until a connection is established
    print('Client:', sc.getpeername()) # Destination IP and port
    t = sc.recv(BUF_SIZE) # recvfrom not needed since address is known
    if t[ -1 ] == b'\n' and len(t) <= 171:
    	print(t)
    	sc.sendall(b'Received ' + t + b'\n') # Destiantion IP and port implicit due to accept call
    	sc.close() # Termination

