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

server_name = "127.0.0.1"
server_port = 12000
size_limit = 4096  # All messages sent must be limited to 4096 bytes
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

while True:
    message = input("Enter Input > ")
    client_socket.send(message.encode())

    if message == "/q":
        print("Quitting...")
        break

    response = client_socket.recv(size_limit).decode()
    if response == "/q":
        print("Server has requested to quit.")
        break
    else:
        print(f"From Server: {response}")

client_socket.close()
print("Connection closed.")