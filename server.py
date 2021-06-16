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
all_players = []
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
    global server, client_name, all_clients, all_clients_threads, all_players, player1, player2
    clients_in_games = []
    client_msg = " "

    # send welcome message to client
    new_client = client_connection.recv(4096).decode(FORMAT)
    new_player_info = json.loads(new_client)

    current_room_id = new_player_info["room_id"]
    current_player_id = new_player_info["player_id"]

    game_info = game_data.find_one({"_id": ObjectId(current_room_id)})
    player1_nick = users_data.find_one({"_id": ObjectId(game_info["u1_id"])})["username"]
    you_are_u1 = False
    #if we are the second player - update database
    if ObjectId(current_player_id) != game_info["u1_id"]:
        game_data.update_one({"_id": "room_id"}, {"$set": {"id_u2": current_player_id}})
    else:
        you_are_u1 = True

    player2_nick = users_data.find_one({"_id": game_info["u2_id"]})["username"]

    your_symbol = "X" if ObjectId(current_player_id) == game_info["u1_id"] else "O"
    your_nick = player1_nick if you_are_u1 else player2_nick
    opponent_nick = player2_nick if your_nick == player1_nick else player1_nick

    ######################################
    current_game_threads = get_current_game_threads(current_room_id, client_connection)
    current_turn = game_info["current_turn"]
    current_game_board = game_data.find_one({"_id": ObjectId(current_room_id)})["moves"]

    #one of the possible starts for player
    if len(current_game_threads) < 2:
        current_game_threads[0].send(json.dumps({"command":"welcome_first_player", "updated_board": current_game_board, "current_turn": current_turn,
                                           "your_symbol": your_symbol, "your_nick": your_nick, "opponent_nick": opponent_nick}).encode(FORMAT))
    else:
        current_game_threads[1].send(json.dumps({"command":"welcome_second_player", "updated_board": current_game_board, "current_turn": current_turn,
                                           "your_symbol": your_symbol, "your_nick": your_nick, "opponent_nick": opponent_nick}).encode(FORMAT))


    while True:
        # get the player choice from received data
        data = client_connection.recv(4096).decode(FORMAT)
        if not data: break
        msg = json.loads(data)
        # player x,y coordinate data. forward to the other player
        if msg["command"] == "new_move":

            # changing turn if last moved symbol is different
            current_turn = game_data.find_one({"_id": ObjectId(current_room_id)})["current_turn"]

            if msg["next_turn_symbol"] != current_turn:
                current_turn = msg["next_turn_symbol"]
                game_data.update_one({"_id": ObjectId(current_room_id)}, {"$set": {"current_turn": current_turn}})

            #updating the board
            if len(msg["updated_board"]) > len(current_game_board):
                game_data.update_one({"_id": ObjectId(current_room_id)}, {"$set": {"moves": msg["updated_board"]}})
                current_game_board = msg["updated_board"]
            else:
                current_game_board = game_data.find_one({"_id": ObjectId(current_room_id)})["moves"]

            #sending data to both clients
            if client_connection == current_game_threads[0]:
                current_game_threads[1].send(json.dumps({"command":"new_move", "updated_board": current_game_board, "current_turn": current_turn}).encode(FORMAT))
            else:
                current_game_threads[0].send(json.dumps({"command":"new_move", "updated_board": current_game_board, "current_turn": current_turn}).encode(FORMAT))

    #sprawdzić na koniec czy wszystko poprawnie usuwa
    #all_clients_threads.remove(client_connection)
    print("current_game_threads BEFORE remove:", current_game_threads)
    current_game_threads.remove(client_connection)
    print("current_game_threads AFTER remove:", current_game_threads, '\n')

    print("all_clients BEFORE remove:", all_clients)
    all_clients.remove(client_connection)
    print("all_clients AFTER remove:", all_clients, '\n')
    client_connection.close()


print("[STARTING] Server is starting...")
start_server()
