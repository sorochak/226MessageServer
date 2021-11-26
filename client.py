#!/usr/bin/env python3

import asyncio
import sys
import random
import string
import time

KEYLENGTH = 8
PUT_CMD = 'PUT'
GET_CMD = 'GET'
PROMPT = 'Please Enter a Message'

def getRandKey():
    str = string.ascii_letters + string.digits
    return ''.join(random.choice(str) for i in range(KEYLENGTH))

def getUserMsg():
    usrMessage = input(PROMPT)
    return usrMessage


async def getMsg(key, reader, writer):
    message = GET_CMD + key + '\n'
    writer.write(message.encode())
    data = await reader.readline()
    data = data.decode()
    writer.close()
    await writer.wait_closed()
    return data

async def putMsg(key, message, reader, writer):
    sendMsg = PUT_CMD + key + '\n'
    writer.write(sendMsg.encode())
    serverResponse = await reader.readline()
    serverResponse = serverResponse.decode()
    writer.close()
    await writer.wait_closed()

async def client(host, port, key):
    
    try:
        mostRecentKey = key.encode('utf-8')
        while True:
            reader, writer = await asyncio.open_connection(host, port)
            writer.write(b'GET' + mostRecentKey + b'\n')
            data = await reader.readline()
            print(data.decode())
            if data != b'\n':
                mostRecentKey = data[:KEYLENGTH]
                print(mostRecentKey)
                message = data[KEYLENGTH:]
                #print(len(data))
            else:
                newMsg = getUserMsg()
                reader, writer = await asyncio.open_connection(host, port)
                writer.write(b'PUT' + mostRecentKey + (getRandKey() + newMsg).encode('utf-8')+ b'\n')
                #await putMsg(key, getRandKey() + newMsg, reader, writer)
                #print('test')
                break
           
    except Exception as error:
       print(error, 123)
    


if len(sys.argv) != 4:
    print(f'{sys.argv[0]} needs 3 argument to transmit')
    sys.exit(-1)

asyncio.run(client(sys.argv[1], sys.argv[2], sys.argv[3]))
