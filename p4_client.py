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


def play_cities_game(client_socket):

    game_start_message = "Starting cities game..."
    print(game_start_message)

    clients_turn= True

    # Client always has the first turn
    while True:

        if clients_turn:  # Client's turn to play

            # Receive the last letter information from the server
            last_letter = client_socket.recv(size_limit).decode()

            if last_letter == "1":
                city_to_send = input("Enter the first city name beginning with any letter > ")
                if city_to_send == "/q":
                    print("Client has requested to quit game and return to chat mode.")
                    print("Quitting game and returning to chat mode...")
                    return
                client_socket.send(city_to_send.encode())
                print("Receiving...")
            else:
                city_to_send = input(f"Enter a city name beginning with {last_letter} > ")
                if city_to_send == "/q":
                    print("Client has requested to quit game and return to chat mode.")
                    print("Quitting game and returning to chat mode...")
                    return
                client_socket.send(city_to_send.encode())
                print("Receiving...")

            validity_message_from_server = client_socket.recv(size_limit).decode()
            if validity_message_from_server == "invalid":
                print("Invalid city name, client loses the game. Returning to chat mode...")
                return
            else:  # validity message from server is valid
                clients_turn = False

        else:  # Server's turn to play
            city_received = client_socket.recv(size_limit).decode()

            if city_received == "/q":
                print("Server has requested to quit game and return to chat mode.")
                return


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
