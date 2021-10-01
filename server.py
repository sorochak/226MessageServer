#!/usr/bin/python3

import socket
import sys

BUF_SIZE = 1024
HOST = ''
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen(1) # Enable server to receive 1 connection at a time
print('Server: ', sock.getsockname()) # Source IP and port

new_dict = {}
while True:
    sc, sockname = sock.accept() # Wait until a connection is established
    print('Client:', sc.getpeername()) # Destination IP and port
    t = sc.recv(BUF_SIZE) # recvfrom not needed since address is known
    
    command = t[:3]
    alphaNumKey = t[3:11].decode().strip()
    message = t[11:].decode().strip()
   
    print(alphaNumKey,command, message, len(message), len(alphaNumKey))

    try:
        if  len(message) <= 160:
            if command == b'PUT':
                if len(alphaNumKey) < 8 or len(message) < 1:
                    sc.sendall(b'NO\n')
                else:
                    new_dict[alphaNumKey] = message
                    sc.sendall(b'OK\n')
            elif command == b'GET':
                if (len(alphaNumKey) < 8) or (len(message) > 0):
                    sc.sendall(b'\n')
                elif alphaNumKey in new_dict:
                    sc.sendall(new_dict.get(alphaNumKey).encode() + b'\n')
                else:
                    sc.sendall(b'\n')
            elif command != b'GET' and command != b'PUT':
                sc.sendall(b'NO\n')
        else:
            sc.sendall(b'NO\n')
    except Exception as error:
       print(error)
    sc.close() # Termination


