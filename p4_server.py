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

from socket import *

def is_valid_city(city, last_letter, valid_cities, used_cities):
    city = city.lower()
    if last_letter != "1":
        return city not in used_cities and city.startswith(last_letter) and city in valid_cities
    else:
        return city not in used_cities and city in valid_cities

def play_cities_game(connection_socket):
    print("Starting cities game...")

    valid_cities = {"new york", "kansas", "seattle", "los angeles", "san francisco", "miami", "dallas", "austin",
                    "boston", "chicago"}
    used_cities = set()
    last_letter = "1"
    servers_turn = False

    while True:
        if not servers_turn:  # Client's turn to play
            connection_socket.send(last_letter.encode())
            city_received = connection_socket.recv(4096).decode().lower()

            if city_received == "/q":
                print("Client requested to quit. Returning to chat mode...")
                return

            if is_valid_city(city_received, last_letter, valid_cities, used_cities):
                used_cities.add(city_received)
                last_letter = city_received[-1]
                servers_turn = True
            else:
                connection_socket.send("invalid".encode())
                print("Invalid city. Client loses. Returning to chat mode...")
                return

        else:  # Server's turn to play
            city_to_send = input(f"Enter a city name starting with '{last_letter}' (or '/q' to quit): ").lower()
            if city_to_send == "/q":
                print("Quitting game. Returning to chat mode...")
                return

            if is_valid_city(city_to_send, last_letter, valid_cities, used_cities):
                used_cities.add(city_to_send)
                last_letter = city_to_send[-1]
                servers_turn = False
                connection_socket.send(city_to_send.encode())
            else:
                print("Invalid city. Server loses. Returning to chat mode...")
                return

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(("", 12000))
    server_socket.listen(1)
    print("Server is waiting for connection...")

    connection_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}. Starting chat mode...")

    while True:
        message_received = connection_socket.recv(4096).decode()
        if message_received == "/q":
            print("Client requested to quit.")
            break
        elif message_received.lower() == "play cities":
            play_cities_game(connection_socket)
        else:
            print(f"Message from client: {message_received}")
            response = input("Enter response (or 'play cities' to start the game): ")
            if response == "/q":
                print("Server quitting.")
                break
            connection_socket.send(response.encode())

    connection_socket.close()
    print("Connection closed. Program terminated.")

if __name__ == "__main__":
    main()