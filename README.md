# Overview

This networking program is a simple client/server chatroom which runs two separate scripts. The host script (server.py) will need to run first on a separate terminal to initialize the server for clients to join into. The client script (client.py) will then need to be run by each "user" who wants to join the chatroom. Note that each of these clients will need to run the script in a separate terminal for them to join the chatroom. 

To describe what this program does, it's simple enough to say that this is a chatroom which supports several special commands and a private chat. The host creates the room for each of the clients to then connect to and interact with each other. Normal messages will be broadcasted to all users for everyone to see. Special commands will display data (like the time, other clients in the room, or help exit the room) upon request. Private chats with one other person in the chat room can also be created using special commands in which only that targeted user will then see your messages to him. Of course, the user can then exit the room whenever he wants without the server going down.

I chose to write this program because I wanted to understand how "networking" actually could connect multiple computers, users, or programs together. This program isn't truly a networking program as it is because it uses my local device in order to run the host and clients, but it can be (somewhat) easily changed to allow foreign computers to run this script as well. Ultimately, I feel like I walked away from this project feeling a lot more confident in understanding how networking can help in future projects. 

[Software Demo Youtube Video](https://youtu.be/Eah9vv7d2kg)

# Network Communication

This program uses the client/server architecture.

Additionally, I used TCP in this program and created a random port at location number 10001. The port number I use really doesn't matter so long as it isn't being used by another other computer functions. To be safe, I chose a number outside of the 1 - 1500 range (because many of those ports are being used for other functions).

The messages are being encoded and decoded from ascii to send first from the client to the host then to all or some other clients. I've done this by using the .send() function followed by the .encode("ascii")/.decode("ascii") "formatting" functions. Both server-side and client-side scripts have methods to "handle" how these messages are sent and received to eliminate errors using try/except statements. (Note: Messages are also received using the .recv() function as well.)

# Development Environment

Tools Used:
* Python v3.8.2
* VSCode

Libraries Used:
* socket
* threading
* datetime

# Useful Websites

Note: The freeCodeCamp tutorial is great for any users who want to create their own chatroom but lack the skeletal framework to do so. It explains how to create proper sockets and connections very simply.

* [General Network Programming Tutorials From freeCodeCamp](https://www.youtube.com/watch?v=FGdiSJakIS4)
* [Python Documentation: Sockets](https://docs.python.org/3.6/library/socket.html)
* [w3schools Python Tutorials](https://www.w3schools.com/python/default.asp)

# Future Work

* Fix the !private command for proper error handling.
* Eliminate some global variables in both server and client scripts
* Upgrade from terminal to GUI
* Include a log so that clients who join late can still see chat history