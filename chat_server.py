#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "[Stack Otterflow]"
__credits__ = [
    "Krishna Tagdiwala",
    "Jorge Vazquez",
    "Walid Elgammal",
    "Jesus Martinez Miranda"
]

import socket as s
import threading

# Configure logging
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

users = []
names = []


def connection_handler(connection_socket, address):

    # Sends the client a welcome message for the chat service
    welcome_message = "Welcome to the chat! To send a message, type the message and click enter."
    connection_socket.send(welcome_message.encode())

    # Asking client for a username and storing it in the local variable username
    connection_socket.send("Enter username: ".encode())
    username = connection_socket.recv(1024).decode()

    # Initializes message to an empty string
    message = ""

    # If the sender sent "bye", server disconnects the sender client
    while message != "bye":
        try:
            # Waits to receive a message from the client
            message = connection_socket.recv(1024).decode()
            # Logs messages exchanged by clients (used for debugging purposes)
            # log.info("Message received by " + address[0] + ". Message: " + message)

            # Checks to see if the client sends "bye"
            # Notifies the other client accordingly
            if message == "bye":
                disconnect_message = f"{username} has left the chat"
                send_message(connection_socket, disconnect_message.encode())
            # Otherwise, the server relays the message sent by the sender client to the receiver client
            else:
                message = f"{username}: {message}"
                send_message(connection_socket, message.encode())
        except:
            print("Exception error when receiving data.")
            break
    # Once user terminates session, close socket
    users.remove(connection_socket)
    connection_socket.close()

# Sends messages from one client to the other client
def send_message(connection_socket, message):
    for socket in users:
        if socket is not connection_socket:
            socket.send(message)


def main():
    # Create a TCP socket
    # Notice the use of SOCK_STREAM for TCP packets
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # Assign port number to socket, and bind to chosen port
    server_socket.bind(('10.0.0.1', server_port))

    # Configure how many requests can be queued on the server at once
    server_socket.listen(1)

    # Alert user we are now online
    log.info("The server is ready to receive on port " + str(server_port))

    # Surround with a try-finally to ensure we clean up the socket after we're done
    try:
        # Enter forever loop to listen for requests
        while True:
            # When a client connects, create a new socket and record their address
            connection_socket, address = server_socket.accept()
            log.info("Connected to client at " + str(address))

            # Keeps track of the connection sockets to relay messages between clients
            users.append(connection_socket)

            # Setting up multiple threads to accept connections
            thread = threading.Thread(target=connection_handler, args=(connection_socket, address))
            thread.start()

            # # Pass the new socket and address off to a connection handler function
            # connection_handler(connection_socket, address)
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
