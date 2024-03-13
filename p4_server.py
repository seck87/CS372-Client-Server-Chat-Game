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

valid_cities = {"new york", "kansas", "seattle", "los angeles", "san francisco", "miami", "dallas", "austin", "boston", "chicago"}

def is_valid_city(city, last_letter, used_cities):
    city = city.lower()
    if last_letter:
        return city not in used_cities and city.startswith(last_letter) and city in valid_cities
    else:
        return city not in used_cities and city in valid_cities


def play_cities_game(connection_socket):
    used_cities = set()
    last_letter = ''
    my_turn = False

    while True:
        if my_turn:
            response = input("Enter a city: ")
            if is_valid_city(response, last_letter, used_cities):
                used_cities.add(response.lower())
                last_letter = response[-1].lower()
                connection_socket.send(response.encode())
            else:
                print("Invalid city. Skipping turn.")
                connection_socket.send("Invalid city. Your turn.".encode())
            my_turn = False
        else:
            message_received = connection_socket.recv(size_limit).decode().lower()
            if message_received == "/q" or message_received == "end game":
                return "/q" if message_received == "/q" else "Exiting game mode."
            elif is_valid_city(message_received, last_letter, used_cities):
                used_cities.add(message_received)
                last_letter = message_received[-1]
                print(f"Client chose: {message_received}")
                my_turn = True
            else:
                warning = "Client provided an invalid city. Server's turn."
                print(warning)
                my_turn = True


server_port = 12000
size_limit = 4096
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", server_port))
server_socket.listen(1)
print("The server is ready to receive")

while True:
    connection_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}.")

    # Initialize chat mode, since the connection is always established by the client they have the first turn
    while True:
        message_received = connection_socket.recv(size_limit).decode()
        if message_received == "/q":
            print("Client has requested to quit.")
            connection_socket.send("/q".encode())  # Send exit message to client to shut down its end
            break
        elif message_received == "play cities":
            print("Switching to Cities game mode.")
            game_response = play_cities_game(connection_socket)
            if game_response == "/q":
                print("Client has requested to quit from game mode.")
                connection_socket.send("/q".encode())
                break
            else:
                connection_socket.send(game_response.encode())
        else:
            print(f"From Client: {message_received}")
            message_to_send = input("Enter Input > ")
            if message_to_send == "/q":
                print("Server has requested to quit.")
                connection_socket.send("/q".encode())  # Send exit message to client to shut down its end
                break
            else:
                connection_socket.send(message_to_send.encode())

    break

connection_socket.close()
print("Connection closed.")
