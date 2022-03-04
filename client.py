import threading
import socket

# When client script is run, prompt for and save user's nickname for later
# Note, change this so it's not global
nickname = input("Enter your nickname: ")

# Create TCP connection and connect specifically to our host's location
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 10001))

def receive():
    # This method will handle receiving messaged from the server (host)

    while True:
        # Error handling
        try:
            message = client.recv(1024).decode("ascii")

            # If the client receives special keywords, perform special action

            # Send host the nickname we made for ourselves
            if message == "NICKNAME":
                client.send(nickname.encode("ascii"))

            # If the host tells us we are exited, kill this loop
            elif message == "EXIT":
                # Notify client we just left
                print("Exited chatroom...")
                client.close()
                break

            # Otherwise, print received message to client
            else:
                print(message)

        # If receiving message failed, exit everything
        except:
            print("An error occurred. Exiting...")
            client.close()
            break

def write():
    # This will send messages written by the client to the server.

    while True:
        user_message = input("")

        # Create special conditions for keywords on client side:

        # If one of these keywords, send raw keyword without formatting
        if user_message in ("!commands", "!time", "!clients"):
            message = user_message
            client.send(message.encode("ascii"))

        # If exit, then send raw message and also break this loop
        elif user_message == "!exit":
            message = user_message
            client.send(message.encode("ascii"))
            break

        # If user prompts for private chatroom, handle differently:
        elif user_message == "!private":
            message = user_message
            client.send(message.encode("ascii"))

            # Prompt user again for who he/she wants to talk to
            nickname_confirm = input("")
            client.send(nickname_confirm.encode("ascii"))

            # Create loop to allow user to solely talk to private chat target. Disables commands and other special keywords
            while True:
                private_input = input("")

                # Allow the user to leave this chatroom on his end and prompt the server to exit as well
                if private_input == "!exit":
                    client.send(private_input.encode("ascii"))
                    print("Exited Private Chat!")
                    break

                # Otherwise, format the message and send to host >> targeted client
                else:
                    formatted_message = f">{nickname}: {private_input}"
                    client.send(formatted_message.encode("ascii"))
        else:
            message = f">{nickname}: {user_message}"
            client.send(message.encode("ascii"))
        

# Create independent threads for both methods here. This is so we can write and receive messages at the same time.
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
