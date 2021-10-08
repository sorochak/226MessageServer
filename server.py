#!/usr/bin/python3

import socket
import sys

BUF_SIZE = 1024
HOST = ''
PORT = 12345
msg_dict = {}
KEYLENGTH = 8
MSGMAXLENGTH = 160
CMD_LENGTH = 3
MSG_INDEX = 11
#
# PURPOSE:
# converts a message to binary before sending
#
# PARAMETERS:
# 'msg' contains the message received from the command

def sendResponse(msg):
    sc.sendall(msg.encode())

#
# PURPOSE:
# sets up a TCP message server
#
# RETURN:
# returns TCP socket

def serverSetup():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Enable server to receive 1 connection at a time
    print('Server: ', sock.getsockname()) # Source IP and port
    return sock

#
# PURPOSE:
# validates key length and message length
# and stores message in a dictionary
# and sends appropriate response based on actions taken
#
# PARAMETERS:
# 'key' contains an alphanumeric key
# 'keyL' contains the constant KEYLENGTH
# 'msg' contains the message
#
# SIDE EFFECTS:
# 'msg_dict' dictionary is updated to store the key and message
#

def putCommand(key, msg):
    if len(key) < KEYLENGTH or len(msg) < 1:
        sendResponse('NO\n')
    else:
        msg_dict[key] = msg
        sendResponse('OK\n')

#
# PURPOSE:
# validates key length and message length
# sends message based on the provided key
# and sends the appropriate response based on actions taken
#
# PARAMETERS:
# 'key' contains an alphanumeric key
# 'keyL' contains the constant KEYLENGTH
# 'msg' contains the message

def getCommand(key, msg):
    if (len(key) < KEYLENGTH) or (len(msg) > 0):
        sendResponse('\n')
    elif key in msg_dict:
        sendResponse(msg_dict.get(key) + '\n')
    else:
        sendResponse('\n')

sock = serverSetup()

while True:
    sc, sockname = sock.accept() # Wait until a connection is established
    print('Client:', sc.getpeername()) # Destination IP and port
    t = sc.recv(BUF_SIZE) # recvfrom not needed since address is known
    
    command = t[:CMD_LENGTH]
    alphaNumKey = t[CMD_LENGTH:MSG_INDEX].decode().strip()
    message = t[MSG_INDEX:].decode().strip()

    try:
        if  len(message) <= MSGMAXLENGTH:
            if command == b'PUT':
                putCommand(alphaNumKey, KEYLENGTH, message)
            elif command == b'GET':
                getCommand(alphaNumKey, KEYLENGTH, message)
            elif command != b'GET' and command != b'PUT':
                sendResponse('NO\n')
        else:
            sendResponse('NO\n')
    except Exception as error:
       print(error)
    sc.close() # Termination


