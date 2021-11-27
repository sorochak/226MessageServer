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

# Global variable key
mostRecentKey = ''

def getRandKey():
    str = string.ascii_letters + string.digits
    return ''.join(random.choice(str) for i in range(KEYLENGTH))

async def getUserMsg():
    loop = asyncio.get_running_loop()
    usrMessage = await loop.run_in_executor(None, input, PROMPT)
    return usrMessage


async def get_message():
    global mostRecentKey
    try:
        mostRecentKey = sys.argv[3].encode('utf-8')
        while(True):
            reader, writer = await asyncio.open_connection(sys.argv[1], sys.argv[2])
            writer.write(b'GET' + mostRecentKey + b'\n')
            await writer.drain()
            data = await reader.readline()
            print(data.decode())
            
            if data == b'':
                await asyncio.sleep(5)
            else:
                mostRecentKey = data[:KEYLENGTH]
                message = data[KEYLENGTH:]
                print(message)
        
    except Exception as error:
        print(error, 123)
    #message = GET_CMD + key + '\n'
    #writer.write(message.encode())
    #data = await reader.readline()
    #data = data.decode()
    #writer.close()
    #await writer.wait_closed()
    #return data

async def put_message():
    #try:
    newKey = mostRecentKey
    while(True):
        reader, writer = await asyncio.open_connection(sys.argv[1], sys.argv[2])
        try:
            newMsg = await getUserMsg()
        except:
            return
        
        writer.write(b'PUT' + newKey + (getRandKey() + newMsg).encode('utf-8') + b'\n')
        await writer.drain()
        data = await reader.readline()
        print(data, 789, data[:2])
        if data[:2] == b'NO':
            print(data[2:])
            newKey = data[2:10]
            #writer.write(b'PUT' + newKey + (getRandKey() + newMsg).encode('utf-8') + b'\n')
            
        writer.close()
        await writer.wait_closed()
    
    print(msg_dict)
        
        #writer.write(b'PUT' + mostRecentKey.encode('utf-8') + (getRandKey() + newMsg).encode('utf-8') + b'\n')
    
    #except Exception as error:
        #print(error, 123)
    #sendMsg = PUT_CMD + key + '\n'
    #writer.write(sendMsg.encode())
    #serverResponse = await reader.readline()
    #serverResponse = serverResponse.decode()
    #writer.close()
    #await writer.wait_closed()

#async def client(host, port, key):
    
    #try:
        #mostRecentKey = key.encode('utf-8')
        #while True:
 
            #if data != b'\n':
                #mostRecentKey = data[:KEYLENGTH]
                #print(mostRecentKey)
                #message = data[KEYLENGTH:]
                #print(len(data))
            #else:
                #newMsg = getUserMsg()
                #reader, writer = await asyncio.open_connection(host, port)
                #writer.write(b'PUT' + mostRecentKey + (getRandKey() + newMsg).encode('utf-8')+ b'\n')
                #await putMsg(key, getRandKey() + newMsg, reader, writer)
                #print('test')
                #break
           
    #except Exception as error:
       #print(error, 123)
       

async def main():
    try:
        await asyncio.gather(get_message(), put_message())
    except Exception as e:
        print(e)
        traceback.print_exc()
    


if len(sys.argv) != 4:
    print(f'{sys.argv[0]} needs 3 argument to transmit')
    sys.exit(-1)

asyncio.run(main())
