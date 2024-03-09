# Name: Murat Seckin Kuvandik
# OSU Email: kuvandim@oregonstate.edu
# Course: CS372
# Citations for the following code structure:
# Date: 03/09/2024
# Copied from /OR/ Adapted from /OR/ Based on:
# Textbook: Computer Networking: A Top-Down Approach 8th Edition, James F. Kurose, Keith W. Ross
# Source URL: https://docs.python.org/3/howto/sockets.html#using-a-socket

from socket import *

server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", server_port))
server_socket.listen(1)
print("The server is ready to receive")

while True:
    connection_socket, addr = server_socket.accept()
    # When a client knocks on this door, the program invokes the accept() method for
    # server_socket, which creates a new socket in the server, called connection_socket,
    # dedicated to this particular client.

    sentence = connection_socket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connection_socket.send(capitalizedSentence.encode())
    connection_socket.close()
