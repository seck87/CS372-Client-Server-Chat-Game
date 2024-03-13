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


def play_cities_game(client_socket):
    print("You have entered the Cities game mode. Type 'end game' to quit the game mode.")
    my_turn = True

    while True:
        if my_turn:
            city = input("Enter a city: ")
            client_socket.send(city.encode())
            if city == "/q" or city == "end game":
                return city
            my_turn = False
        else:
            response = client_socket.recv(size_limit).decode()
            if response == "/q":
                return response
            print(f"Server's choice or message: {response}")
            my_turn = True


server_name = "127.0.0.1"
server_port = 12000
size_limit = 4096  # All messages sent must be limited to 4096 bytes
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

while True:
    message_to_send = input("Enter Input (or 'play cities' to start the game) > ")
    client_socket.send(message_to_send.encode())

    if message_to_send == "/q":
        print("Client has requested to quit.")
        break
    elif message_to_send == "play cities":
        game_exit_code = play_cities_game(client_socket)
        if game_exit_code == "/q":
            print("Quitting from game mode...")
            break
        elif game_exit_code == "end game":
            print("Exiting game mode, back to chat.")
            response = client_socket.recv(size_limit).decode()
            print(f"Response: {response}")
    else:
        response = client_socket.recv(size_limit).decode()
        if response == "/q":
            print("Server has requested to quit.")
            break
        else:
            print(f"From Server: {response}")

client_socket.close()
print("Connection closed.")
