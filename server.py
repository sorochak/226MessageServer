#!/usr/bin/python3

import sys
import traceback
import asyncio

BUF_SIZE = 1024
HOST = ''
PORT = 12345
msg_dict = {}
KEYLENGTH = 8
MSGMAXLENGTH = 160
CMD_LENGTH = 3
MSG_INDEX = 11
PUT_CMD = 'PUT'
GET_CMD = 'GET'
OK_MSG = b'OK\n'
NO_MSG = b'NO\n'
NEWLINE = b'\n'


def sendResponse(s, writer):
    writer.write(s)


#
# PURPOSE:
# validates key length and message length
# and stores message in a dictionary
# Sends 'NO\n' message if key length is less than KEYLENGTH or if length of msg is < 1
# 
#
# PARAMETERS:
# 'key' contains an alphanumeric key
# 'msg' contains the message
# 'sc' contains a valid server socket
#
# SIDE EFFECTS:
# 'msg_dict' dictionary is updated to store the key and message
#

def putCommand(key, msg, writer):
    if len(key) < KEYLENGTH or len(msg) < 1:
        sendResponse(NO_MSG, writer)
    else:
        msg_dict[key] = msg
        sendResponse(OK_MSG, writer)

#
# PURPOSE:
# validates key length and message length
# sends message based on the provided key
# and sends the appropriate response based on actions taken
#
# PARAMETERS:
# 'key' contains an alphanumeric key
# 'msg' contains the message
# 'sc' contains a valid server socket

def getCommand(key, msg, writer):
    if (len(key) < KEYLENGTH) or (len(msg) > 0):
        sendResponse(NEWLINE, writer)
    elif key in msg_dict:
        print('get', key, msg_dict.get(key))
        sendResponse(msg_dict.get(key).encode() + NEWLINE, writer)
    else:
        sendResponse(NEWLINE, writer)


#
# PURPOSE:
# Given a valid server socket, gets a line from the socket,
# extracts a command, key, and message.
# if PUT command is received, calls putCommand()
# if GET command is received, calls getCommand()
# if neither PUT or GET is received sends 'NO\n' response
#
# PARAMETERS:
# 'sc' contains a valid server socket
#
# NOTES:
# Connection errors are handled
#

async def process_command(reader, writer):
    d = await reader.readline()
    t = d.decode('utf-8').strip()
    command = t[:CMD_LENGTH]
    alphaNumKey = t[CMD_LENGTH:MSG_INDEX]
    message = t[MSG_INDEX:]

    try:
        if  len(message) <= MSGMAXLENGTH:
            if command == PUT_CMD:
                putCommand(alphaNumKey, message, writer)
            elif command == GET_CMD:
                getCommand(alphaNumKey, message, writer)
            elif command != GET_CMD and command != PUT_CMD:
                sendResponse(NO_MSG, writer)
        else:
            sendResponse(NO_MSG, writer)
    except Exception as error:
       print(error)
       traceback.print_exc()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(process_command, '', 12345)
    await server.serve_forever() # without this, program terminates

asyncio.run(main())


