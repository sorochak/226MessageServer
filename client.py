#!/usr/bin/env python3

import asyncio
import sys
import random
import string
import time
import traceback

KEYLENGTH = 8
PUT_CMD = 'PUT'
GET_CMD = 'GET'
PROMPT = 'Please Enter a Message \n'
NUM_ARGS = 4
HOST_ARG = 1
PORT_ARG = 2
KEY_ARG = 3
WAIT = 5

# Global variables for keys
nextGetKey = ''
nextPutKey = ''

def getRandKey():
    str = string.ascii_letters + string.digits
    return ''.join(random.choice(str) for i in range(KEYLENGTH))

# async def getUserMsg():
#     loop = asyncio.get_running_loop()
#     usrMessage = await loop.run_in_executor(None, input, PROMPT)
#     return usrMessage


async def get_message():
    global nextGetKey, nextPutKey
    
    while(True):
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(b'GET' + nextGetKey + b'\n')
        data = await reader.read()
        #print(data.decode())
        writer.close()
        await writer.wait_closed()
        
        if data == b'\n':
            nextPutKey = nextGetKey
            await asyncio.sleep(WAIT)
            continue

        if len(data) < KEYLENGTH:
            print('**** Error', data)
            break
        
        nextGetKey = data[:KEYLENGTH]
        message = data[KEYLENGTH:]
        print('             ', '>', message)

async def put_message():
    global nextPutKey

    loop = asyncio.get_running_loop()

    while True:
        try:
            nextMessage = await loop.run_in_executor(None, input, "<    ")
            nextMessage = nextMessage.encode()
        except Exception as e:
            print(e)
            break
        
        nextProposedKey = ''.join(random.choices(string.ascii_letters + string.digits, k = KEYLENGTH)).encode()
        while True:
            reader, writer = await asyncio.open_connection(host, port)
            writer.write(b'PUT' + nextPutKey + nextProposedKey + nextMessage + b'\n')
            data = await reader.read()
            writer.close()
            await writer.wait_closed()
            #print('REPLY   ', data)

            if data[:2] == b'OK':
                print()
                break
            if data[:2] == b'NO':
                nextPutKey = data[2:10]
                continue
            if len(data) < 10:
                print('**** Size Error', data)
                break
            print('**** Unexpected Error', data)
            break
        

async def main():
    try:
        await asyncio.gather(get_message(), put_message())
    except Exception as e:
        print(e)
        traceback.print_exc()
    

if len(sys.argv) != NUM_ARGS:
    print(f'{sys.argv[0]} needs 3 argument to transmit')
    sys.exit(-1)

host = sys.argv[HOST_ARG]
port = sys.argv[PORT_ARG]
key = sys.argv[KEY_ARG]
nextGetKey = key.encode('utf-8')
nextPutKey = nextGetKey
asyncio.run(main())
