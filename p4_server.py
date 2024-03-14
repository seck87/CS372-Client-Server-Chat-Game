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
size_limit = 4096

def is_valid_city(city, last_letter, valid_cities, used_cities):
    city = city.lower()
    if last_letter != "1":
        return city not in used_cities and city.startswith(last_letter) and city in valid_cities
    else:
        return city not in used_cities and city in valid_cities


def play_cities_game(connection_socket):

    game_start_message = "Starting cities game..."
    print(game_start_message)

    valid_cities = {"new york", "kansas", "seattle", "los angeles", "san francisco", "miami", "dallas", "austin",
                    "boston", "chicago"}
    used_cities = set()

    last_letter = "1"
    servers_turn = False

    while True:

        if not servers_turn:  # Client's turn to play
            # Inform the client about the last letter
            connection_socket.send(last_letter.encode())
            city_received = connection_socket.recv(size_limit).decode()

            if city_received == "/q":
                print("Client has requested to quit game and return to chat mode.")
                print("Quitting game and returning to chat mode...")
                return

            if is_valid_city(city_received, last_letter, valid_cities, used_cities):
                used_cities.add(city_received.lower())
                last_letter = city_received[-1].lower()
                servers_turn = True
            else:
                city_validity = "invalid"
                connection_socket.send(city_validity.encode())
                print("Invalid city name, client loses the game. Returning to chat mode...")
                return

        else:  # Server's turn to play
            city_to_send = input(f"Enter a city name beginning with {last_letter} > ")

            if city_to_send == "/q":
                print("Server has requested to quit game and return to chat mode.")
                print("Quitting game and returning to chat mode...")
                return

            if is_valid_city(city_to_send, last_letter, valid_cities, used_cities):
                used_cities.add(city_to_send.lower())
                last_letter = city_to_send[-1].lower()
                servers_turn = False
                print("Receiving...")
            else:
                city_validity = "invalid"
                connection_socket.send(city_validity.encode())
                print("Invalid city name, server loses the game. Returning to chat mode...")
                return



server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", server_port))
server_socket.listen(1)
print("Server is waiting for connection...")

connection_socket, addr = server_socket.accept()
print(f"Connection established with {addr}.")
print("Starting chat mode...")

# Initialize chat mode, since the connection is always established by the client they have the first turn
while True:

    print("Receiving...")
    message_received = connection_socket.recv(size_limit).decode()
    if message_received == "/q":
        print("Client has requested to quit.")
        connection_socket.send("/q".encode())  # Send exit message to client to shut it down
        break
    elif message_received == "play cities":
        print("Client has requested to play cities.")
        play_cities_game(connection_socket)
        print("Starting chat mode...")
    else:
        print(f"Message from client: {message_received}")
        message_to_send = input("Enter Input (or 'play cities' to start the game) > ")
        if message_to_send == "/q":
            print("Server has requested to quit.")
            connection_socket.send("/q".encode())  # Send exit message to client to shut down its end
            break
        elif message_to_send == "play cities":
            print("Server has requested to play cities.")
            connection_socket.send(message_to_send.encode())
            play_cities_game(connection_socket)
            print("Starting chat mode...")
        else:
            connection_socket.send(message_to_send.encode())

connection_socket.close()
print("Connection closed, program terminated.")
