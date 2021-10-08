#!/usr/bin/python3

import socket
import sys
import threading
import traceback

BUF_SIZE = 1024
HOST = ''
PORT = 12345
msg_dict = {}
KEYLENGTH = 8
MSGMAXLENGTH = 160
CMD_LENGTH = 3
MSG_INDEX = 11

locks = threading.Semaphore()

#
# PURPOSE:
# converts a message to binary before sending
#
# PARAMETERS:
# 'msg' contains the message received from the command

def sendResponse(msg, sc):
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

def putCommand(key, msg, sc):
    if len(key) < KEYLENGTH or len(msg) < 1:
        sendResponse('NO\n', sc)
    else:
        locks.acquire()
        msg_dict[key] = msg
        locks.release()
        sendResponse('OK\n', sc)

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

def getCommand(key, msg, sc):
    if (len(key) < KEYLENGTH) or (len(msg) > 0):
        sendResponse('\n', sc)
    elif key in msg_dict:
        locks.acquire()
        sendResponse(msg_dict.get(key) + '\n', sc)
        locks.release()
    else:
        sendResponse('\n', sc)

sock = serverSetup()

def get_line(sc):
    buffer = b''
    size = 0
    while True:
        data = sc.recv(1)
        size += 1
        if data == b'\n' or size >= BUF_SIZE:
            return buffer
        buffer = buffer + data

def process_command(sc, current_socket):
    t = get_line(sc)
    command = t[:CMD_LENGTH]
    alphaNumKey = t[CMD_LENGTH:MSG_INDEX].decode().strip()
    message = t[MSG_INDEX:].decode().strip()

    try:
        if  len(message) <= MSGMAXLENGTH:
            if command == b'PUT':
                putCommand(alphaNumKey, message, sc)
            elif command == b'GET':
                getCommand(alphaNumKey, message, sc)
            elif command != b'GET' and command != b'PUT':
                sendResponse('NO\n', sc)
        else:
            sendResponse('NO\n', sc)
    except Exception as error:
       print(error)
       traceback.print_exc()
    sc.close() # Termination

while True:
    sc, sockname = sock.accept() # Wait until a connection is established
    print('Client:', sc.getpeername()) # Destination IP and port
    threading.Thread(target = process_command, args = (sc, sock, )).start()


