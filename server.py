import socket
import threading
import json
from time import sleep
from db_connection import *


server = None
#HOST_ADDR = socket.gethostbyname(socket.gethostname())
SERVER = '127.0.0.1'
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client_name = " "
all_clients = []
all_games = []
all_clients_threads = []


# Start server functionrecv
def start_server():
    global server, SERVER, PORT # code is fine without this

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)
    server.listen()  # server is listening for client connection
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        client_socket, ip = server.accept()
        all_clients.append(client_socket)
        threading._start_new_thread(send_receive_client_message, (client_socket, ip))


def get_current_game(current_room_id, current_player_id):
    global all_games

    if not any(current_room_id in room_id for room_id in all_games):
        all_games.append({current_room_id: [current_player_id]})

    for game in all_games:
        if current_room_id in game:
            current_game = game[current_room_id]

    if current_player_id not in current_game and len(current_game) < 2:
        current_game.append(current_player_id)

    return current_game


def get_current_game_threads(current_room_id, client_connection):
    global all_clients_threads

    if not any(current_room_id in room_id for room_id in all_clients_threads):
        all_clients_threads.append({current_room_id: [client_connection]})

    for client_in_game in all_clients_threads:
        if current_room_id in client_in_game:
            current_game_threads = client_in_game[current_room_id]

    if client_connection not in current_game_threads and len(current_game_threads) < 2:
        current_game_threads.append(client_connection)

    return current_game_threads


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, all_clients, all_clients_threads, all_games, player1, player2
    clients_in_games = []
    client_msg = " "

    # send welcome message to client
    new_client = client_connection.recv(4096).decode(FORMAT)
    new_player_info = json.loads(new_client)

    current_room_id = new_player_info["room_id"]
    current_player_id = new_player_info["player_id"]

    game_info = game_data.find_one({"_id": ObjectId(current_room_id)})
    player1_nick = users_data.find_one({"_id": ObjectId(game_info["u1_id"])})["username"]

    if current_player_id != game_data.find_one({"_id": ObjectId(current_room_id)})["u1_id"]:
        game_data.update_one({"_id": "room_id"}, {"$set": {"id_u2": current_player_id}})

    player2_nick = users_data.find_one({"_id": ObjectId(game_info["u2_id"])})["username"]

    ######################################
    current_game = get_current_game(current_room_id, current_player_id)
    current_game_threads = get_current_game_threads(current_room_id, client_connection)

    if len(current_game) < 2:
        client_connection.send("welcome_first_player".encode(FORMAT))
    else:
        client_connection.send("welcome_second_player".encode(FORMAT))

    #################################################
    if len(current_game) > 1:
        sleep(1)
        # send opponent name and symbol
        symbols = ["X", "O"]
        # current_game_threads[0].send(("opponent_name$" + player2_nick + "symbol" + symbols[0]).encode(FORMAT))
        # current_game_threads[1].send(("opponent_name$" + player1_nick + "symbol" + symbols[1]).encode(FORMAT))
        current_game_threads[0].send(("opponent_name$" + player2_nick + "symbol" + symbols[1]).encode(FORMAT))
        current_game_threads[1].send(("opponent_name$" + player1_nick + "symbol" + symbols[0]).encode(FORMAT))

    while True:
        # get the player choice from received data
        data = client_connection.recv(4096).decode(FORMAT)
        if not data: break

        # player x,y coordinate data. forward to the other player
        if data.startswith("$xy$"):
            # is the message from client1 or client2?
            if client_connection == current_game_threads[0]:
                # send the data from this player (client) to the other player (client)
                current_game_threads[1].send(data.encode(FORMAT))
            else:
                # send the data from this player (client) to the other player (client)
                current_game_threads[0].send(data.encode(FORMAT))

    #all_clients_threads.remove(client_connection)
    all_clients.remove(client_connection)
    current_game.remove(current_player_id)
    current_game_threads.remove(client_connection)
    client_connection.close()


print("[STARTING] Server is starting...")
start_server()
