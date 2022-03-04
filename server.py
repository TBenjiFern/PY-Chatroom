import socket
import threading
from datetime import datetime

# Define a host (in this case, this identifies my own device as the host)
host = '127.0.0.1'
# Ports 1 - 1024 are used for other functions, so any number past that is okay to use
port = 10001

# We are creating a TCP connection using SOCK_STREAM, and AF_INET is the standard socket to use here
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# We are hooking the server to our host and port we defined above
server.bind((host, port))
# Setting the server we just created to wait for us to do something with it
server.listen()

# These will keep track of who joins our server and the names they give themselves
# Note, I don't like these being global variables, so I would fix these later to be passed in
clients = []
nicknames = []

# Extra Support Commands (Non-critical for chat room to work)
# -----------------------------------------------------------------------------------------------

def display_commands(client):
    # This will display the following commands and their functions to the user upon request
    # !exit, !time, !clients, !private

    client.send("'!exit': Exits the chatroom.\n'!time': Displays current time.\n'!clients': Displays every person on the server.\n'!private': Prompts user for other client nickname and opens private chat.".encode("ascii"))

def display_time(client):
    # Leveraging the datetime library, we are grabbing the current time, formatting it, then printing it to the user

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    client.send(f"Current Time: {current_time}".encode("ascii"))

def display_clients(client):
    # This will loop through the nicknames list and send each nickname to the client's terminal

    for nick in nicknames:
        client.send(f"{nick}\n".encode("ascii"))

def private_chat(client):
    # This method will enable a user to start a private chat with one other user in the chat room

    # This variable will let us escape the private chat on the server side.
    chat_cont = True 

    # This message is unnecessary, but it's nice to see if a private chat correctly opened on the server side or not
    print("Private chat started")

    # Prompt user for a person to talk to (prompts for nickname)
    client.send("Who do you want to talk to?".encode("ascii"))

    # In case the receive fails, handle that case
    try:
        message = client.recv(1024).decode("ascii")

        # If the message they send back is in the nicknames list,
        if message in nicknames:

            # Search up the index number of that person's nickname
            index = nicknames.index(message)

            # Because the actual client information is found at the same index in the clients list
            target = clients[index]

            # Make a private chat room with the target client until the user indicates otherwise
            while chat_cont:

                # Handle possible message error
                try:
                    secret_message = client.recv(1024).decode("ascii")

                    # Allow the user to exit with a command to close the private chat room
                    if secret_message == "!exit":
                        # Server side notify room closed, exit loop, back out of this method
                        print("A private chat closed!")
                        chat_cont = False
                        break
                    else:
                        # Otherwise, send message to targeted client
                        target.send(secret_message.encode("ascii"))
                except:
                    # If error, notify client that the room was terminated
                    # ADD FIX HERE: The private room on the client's side doesn't terminate correctly yet... Add fix here.
                    client.send("Error Detected: Chat terminated".encode("ascii"))
                    # client.send("END_CHAT".encode("ascii"))
                    chat_cont = False
                    break
        else:
            # Note: This also doesn't terminate the private room on the client's side... Add fix here.
            print("Nickname not found in private chat.")
            # client.send("NO_NICK".encode("ascii"))
    except:
        # Note: The user will enter a private chat room on the client side regardless if it initiates on the server side or not.
        # Add fix here as well
        print("Private chat request failed.")

# -----------------------------------------------------------------------------------------------

def broadcast(message):
    # This method will take any message and send it to everyone in the chat room

    for client in clients:
        client.send(message)

def handle(client):
    # This will receive the messages the clients send and then decide what to do with it

    # Loop until the user disconnects or until there is an error
    while True:

        # Handle errors in receiving messages
        try:
            message = client.recv(1024).decode("ascii")

            # Create multiple options for additional commands the user might send (Wish I could use a switch-case here)
            # Display all commands to user
            if message == "!commands":
                display_commands(client)

            # Let the user exit the chatroom
            elif message == "!exit":
                # Send keyword to the client so they exit on their end as well
                client.send("EXIT".encode("ascii"))
                # Find user and remove their info from clients and nicknames lists
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                # Server side notification
                print(f"{nickname} disconnected")
                # Let everyone in chat know this client left
                broadcast(f"{nickname} left the chat.".encode("ascii"))
                nicknames.remove(nickname)
                break

            # Display time to the user
            elif message == "!time":
                display_time(client)

            # Display all clients currently in the chatroom to the user
            elif message == "!clients":
                display_clients(client)

            # Initiate a private chat room with another user
            elif message == "!private":
                private_chat(client)

            # Otherwise, broadcast the message as public to everyone
            else:
                broadcast(message.encode("ascii"))

        # If there is an error, just eliminate the client and kick him from the server
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f"{nickname} disconnected")
            broadcast(f"{nickname} left the chat.".encode("ascii"))
            nicknames.remove(nickname)
            break

def receive():
    # Receive initial information from user once they join the server (set up nickname)

    while True:
        # Receive the client's "address" and "target information" with server.accept()
        client, address = server.accept()

        # Server side notification someone connected
        print(f"Connected with {str(address)}")

        # Prompt user for a nickname right away and save it along with the client at the same index
        client.send("NICKNAME".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        # Create server side notification and broadcast to entire chatroom that so-and-so just joined.
        print(f"Nickname of client is {nickname}.")
        broadcast(f"{nickname} has joined the chat.".encode("ascii"))

        # Notify client that he is connect and how to look up special commands
        client.send("Connected to the server!\n".encode("ascii"))
        client.send("Type '!commands' to display list of special commands.".encode("ascii"))

        # Give this client his own thread to handle him independently. Theoretically, this host can handle multiple messages
        # at the same time with this threading.
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def chat_host():
    # Initialize server with this "main" method
    print("Server is online...")
    receive()

# Run this script if run in terminal
if __name__ == '__main__':
    chat_host()