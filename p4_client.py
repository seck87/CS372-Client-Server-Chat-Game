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

    game_start_message = "Starting cities game..."
    print(game_start_message)



    # my_turn = True
    #
    # while True:
    #     if my_turn:
    #         city = input("Enter a city: ")
    #         client_socket.send(city.encode())
    #         if city == "/q" or city == "end game":
    #             return city
    #         my_turn = False
    #     else:
    #         response = client_socket.recv(size_limit).decode()
    #         if response == "/q":
    #             return response
    #         print(f"Server's choice or message: {response}")
    #         my_turn = True


server_name = "127.0.0.1"
server_port = 12000
size_limit = 4096  # All messages sent must be limited to 4096 bytes
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

print("Starting chat mode...")
while True:

    message_to_send = input("Enter Input (or 'play cities' to start the game) > ")
    client_socket.send(message_to_send.encode())
    print("Receiving...")

    if message_to_send == "/q":
        print("Client has requested to quit.")
        client_socket.send("/q".encode())  # Send exit message to server to shut it down
        break
    elif message_to_send == "play cities":
        print("Client has requested to play cities.")
        play_cities_game(client_socket)
        print("Starting chat mode...")
    else:
        message_received = client_socket.recv(size_limit).decode()
        if message_received == "/q":
            print("Server has requested to quit.")
            break
        elif message_received == "play cities":
            print("Server has requested to play cities.")
            play_cities_game(client_socket)
            print("Starting chat mode...")
        else:
            print(f"Message from server: {message_received}")

client_socket.close()
print("Connection closed, program terminated.")
