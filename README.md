# Asynchronous Client/Server using Python

In my *Network and Server-Side Programming* course at Camosun College, we implemented, tested, and deployed client/server programs in a variety of languages and platforms.

The task for this project was to write a message server and client using the Python asyncio library.
GitHub Actions were used for automatic testing when pushing the project to a remote repository.

Specified requirements for the client behavior include the following:

1. When launched, the client gets a server IP, a server port, and an initial 8-digit key from the command line
2. The client then attempts to get a message with the given key from the given server at the given port
3. If there is a message, assume the message consists of an 8-digit key (call it next-key) and a message body. The message
   body is displayed and the client repeats step 2 with the next key as the given key
4. If there is no message, the next key is the last given key (this could be the initial key)
5. The client polls the server every 5 seconds to see if someone else has deposited a message using the latest key; 
   if so, the message is displayed and the latest key is updated
6. If the user entered a message, sends that message to the server with the latest key; 
   if someone else already used that key, retries with the key provided by the server (this last part must be repeated until the message is successfully delivered)
7. The client does not quit
