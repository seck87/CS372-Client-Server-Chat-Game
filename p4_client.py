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
    print("Starting cities game...")
    clients_turn = True

    while True:

        if clients_turn:

            last_letter = client_socket.recv(4096).decode()

            if last_letter == "1":
                prompt = "Enter the first city name starting with any letter: "
            else:
                prompt = f"Enter a city name starting with '{last_letter}' (or '/q' to quit): "

            city_to_send = input(prompt).lower()

            if city_to_send == "/q":
                print("Quitting game. Returning to chat mode...")
                client_socket.send(city_to_send.encode())
                return

            client_socket.send(city_to_send.encode())
            message_from_server = client_socket.recv(4096).decode()

            if message_from_server == "/q":
                print("Server has requested to quit, returning to chat mode...")
                return

            if message_from_server == "invalid":
                print("Invalid city name by server. You win. Returning to chat mode...")
                return


def main():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12000))

    print("Connected to the server. Starting chat mode...")
    while True:
        message_to_send = input("Enter message (or 'play cities' to start the game): ").lower()
        client_socket.send(message_to_send.encode())

        if message_to_send == "/q":
            print("Client quitting.")
            break
        elif message_to_send == "play cities":
            play_cities_game(client_socket)
        else:
            message_received = client_socket.recv(4096).decode()
            if message_received == "/q":
                print("Server requested to quit.")
                break
            else:
                print(f"Message from server: {message_received}")

    client_socket.close()
    print("Connection closed. Program terminated.")


if __name__ == "__main__":
    main()
