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
import time
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
    message = ""

    while message != "bye":
        try:
            message = connection_socket.recv(1024).decode()
            if message != "bye":
              send_message(connection_socket, message.encode())
        except:
            print("Exception error when receiving data.")

    users.remove(connection_socket)
    connection_socket.close()


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
