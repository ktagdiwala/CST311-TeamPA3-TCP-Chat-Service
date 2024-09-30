#!env python

"""Chat client for CST311 Programming Assignment 3"""
__author__ = "[Stack Otterflow]"
__credits__ = [
    "Krishna Tagdiwala",
    "Jorge Vazquez",
    "Walid Elgammal",
    "Jesus Martinez Miranda"
]

# Import statements
import socket as s

# Configure logging
import logging
import threading

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = '10.0.0.2'
server_port = 12000


def main():
    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    try:
        # Establish TCP connection
        client_socket.connect((server_name, server_port))
    except Exception as e:
        log.exception(e)
        log.error("***Advice:***")
        if isinstance(e, s.gaierror):
            log.error("\tCheck that server_name and server_port are set correctly.")
        elif isinstance(e, ConnectionRefusedError):
            log.error("\tCheck that server is running and the address is correct")
        else:
            log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
        exit(8)

    sending_thread = threading.Thread(target=send_message, args=(client_socket,))
    receiving_thread = threading.Thread(target=recieve_message, args=(client_socket,))
    sending_thread.start()
    receiving_thread.start()
    sending_thread.join()
    receiving_thread.join()

    # # Get input from user
    # user_input = input('Input lowercase sentence:')
    #
    # while user_input != "bye":
    #     # Wrap in a try-finally to ensure the socket is properly closed regardless of errors
    #     try:
    #         # Set data across socket to server
    #         #  Note: encode() converts the string to UTF-8 for transmission
    #         client_socket.send(user_input.encode())
    #
    #         # Read response from server
    #         server_response = client_socket.recv(1024)
    #         # Decode server response from UTF-8 bytestream
    #         server_response_decoded = server_response.decode()
    #
    #         # Print output from server
    #         print('From Server:')
    #         print(server_response_decoded)
    #         # Get input from user
    #         user_input = input('Input lowercase sentence:')
    #     except:
    #         print("Exception occurred when sending message")
    #
    # client_socket.close()


def send_message(client_socket):

    message = ""

    while message != "bye":
      message = input('')
      client_socket.send(message.encode())
    
    client_socket.close()


def recieve_message(client_socket):

  response = ""
  while (response != "bye"):
    response = client_socket.recv(1024)
    response_decoded = response.decode()

    print("Other user said: " + response_decoded)

  print("Other user has left the chat.")


# This helps shield code from running when we import the module
if __name__ == "__main__":
    main()
