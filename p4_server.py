# Name: Murat Seckin Kuvandik
# OSU Email: kuvandim@oregonstate.edu
# Course: CS372
# Citations for the following code structure:
# Date: 03/09/2024
# Copied from /OR/ Adapted from /OR/ Based on:
# Textbook: Computer Networking: A Top-Down Approach 8th Edition, James F. Kurose, Keith W. Ross
# Source URL: https://docs.python.org/3/howto/sockets.html#using-a-socket
# Source URL: https://realpython.com/python-sockets/

from socket import *

server_port = 12000
size_limit = 4096  # All messages sent must be limited to 4096 bytes
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", server_port))
server_socket.listen(1)
print("The server is ready to receive")

while True:
    connection_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")
    # When a client knocks on this door, the program invokes the accept() method for
    # server_socket, which creates a new socket in the server, called connection_socket,
    # dedicated to this particular client.

    while True:
        message = connection_socket.recv(size_limit).decode()
        if message == "/q":
            print("Client has requested to quit.")
            connection_socket.send("/q".encode())
            break
        else:
            print(f"From Client: {message}")
            response = input("Enter Response > ")
            connection_socket.send(response.encode())

    connection_socket.close()
    print("Connection closed.")
