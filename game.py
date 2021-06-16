from tkinter import *
from tkinter import ttk, messagebox
import socket
from time import sleep
import threading
import json
from db_connection import *

# network client
client = None
SERVER = '127.0.0.1'
PORT = 5050
FORMAT = 'utf-8'

list_labels = []
board_checked_fields = []
num_cols = 3
your_turn = False

your_details = {
    "name": "Charles",
    "symbol": "X",
    "color": "",
    "score": 0
}

opponent_details = {
    "name": " ",
    "symbol": "O",
    "color": "",
    "score": 0
}

# MAIN GAME WINDOW
window = Tk()
window.title("Tic-Tac-Toe by Jędrzej Jagiełło")
content = Frame(window)
content.grid(row=0, column=0)

gameInfo = ttk.Frame(content, width=600, height=150)
gameBoard = ttk.Frame(content, borderwidth=5, relief="ridge", width=450, height=450)
gamePoints = ttk.Frame(content, borderwidth=5, relief="ridge", width=150, height=50)
gameHistory = ttk.Frame(content, borderwidth=5, relief="ridge", width=150, height=150)

gameInfo.grid(column=0, row=0, columnspan=2)
gameBoard.grid(column=0, row=1, rowspan=2)
gamePoints.grid(column=1, row=1)
gameHistory.grid(column=1, row=2)

# self.chance_label = ttk.Label(self.gameInfo, text=self.symbol + "'s Chance").grid(row=0, pady="3")
# ttk.Label(gameInfo, text='{} (X) VS {} (O)'.format(u1_nick, u2_nick), font=('arial', 15, 'bold')).grid(row=1, pady="3")
lbl_status = ttk.Label(gameInfo, text="Status: Not connected to server", font="Helvetica 14 bold")
lbl_status.grid(row=1, pady="3")

ttk.Label(gamePoints, text="Score:").grid(row=1)
# ttk.Label(gamePoints, text="{}: {}".format(your_details["name"], users_data.find_one({"username": your_details["name"]})["points"])).grid(
#     row=2)
# ttk.Label(gamePoints, text="{}: {}".format(opponent_details["name"], users_data.find_one({"username": opponent_details["name"]})["points"])).grid(
#     row=2)
ttk.Label(gamePoints, text="{}: {}".format(your_details["name"], "200")).grid(
    row=2)
ttk.Label(gamePoints, text="{}: {}".format(opponent_details["name"], "100")).grid(
    row=2)

ttk.Label(gameHistory, text="Round history:").grid(row=1)
ttk.Label(gameHistory, text="Player1: 1, 1").grid(row=2)
ttk.Label(gameHistory, text="Player2: 3, 1").grid(row=3)

buttonsList = [[], [], []]
for i in range(3):
    for j in range(3):
        buttonsList[i].append(
            Button(gameBoard, text="   ", width=3, padx=5, bd=5, bg="gold2", font=('arial', 60, 'bold'), relief="sunken"))
        buttonsList[i][j].config(command=lambda row=i, col=j: click(row, col))
        buttonsList[i][j].grid(row=i, column=j)


def click(row, col):
    global your_turn, board_checked_fields
    if your_turn == True:
        new_move = {"row": row, "col": col, "symbol": your_details["symbol"]}

        if board_checked_fields == []:
            board_checked_fields = [new_move]
        else:
            board_checked_fields.append(new_move)

        buttonsList[row][col].config(text=your_details["symbol"], state=DISABLED, disabledforeground=your_details["color"])
        your_turn = False

        #check_result()

        client.send(json.dumps({"command": "new_move", "updated_board": board_checked_fields, "next_turn_symbol": opponent_details["symbol"]}).encode(FORMAT))
        lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn! (" + opponent_details["symbol"] + ")"

    # check()  # wysłanie informacji na server
    # changePlayer()


def update_board(updated_board):
    global your_turn, your_details, board_checked_fields
    if len(updated_board) > len(board_checked_fields):
        board_checked_fields = updated_board

    for single_move in board_checked_fields:
        color = your_details["color"] if single_move["symbol"] == your_details["symbol"] else opponent_details["color"]
        buttonsList[single_move["row"]][single_move["col"]].config(text=single_move["symbol"], state=DISABLED, disabledforeground=color)


def connect_to_server(game_data):
    global client, PORT, SERVER
    game_data = json.dumps(game_data)

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client.send(game_data.encode(FORMAT))
        threading._start_new_thread(receive_message_from_server, (client, "m"))


    except Exception as e:
        messagebox.showerror(title="ERROR!!!", message=e)
        # tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + SERVER + " on port: " + str(
        #     PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(client_socket, m):
    global your_details, opponent_details, your_turn
    while True:
        from_server = client_socket.recv(4096).decode(FORMAT)
        if not from_server: break

        msg = json.loads(from_server)

        if msg["command"].startswith("welcome"):
            your_details["symbol"] = msg["your_symbol"]

            if your_details["symbol"] == "X":
                opponent_details["symbol"] = "O"
            else:
                opponent_details["symbol"] = "X"

            if msg["opponent_nick"] != "":
                opponent_details["name"] = msg["opponent_nick"]

            #if it's continuation of the game
            if msg["current_turn"] == your_details["symbol"]:
                your_turn = True
                if len(msg["updated_board"]) > 0:
                    lbl_status["text"] = "STATUS: Your turn! (" + your_details["symbol"] + ")"
            else:
                your_turn = False
                if len(msg["updated_board"]) > 0:
                    lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn! (" + opponent_details["symbol"] + ")"

            if msg["command"] == "welcome_first_player":
                your_details["color"] = "firebrick3"
                opponent_details["color"] = "Dodgerblue2"
                if len(msg["updated_board"]) == 0:
                    lbl_status["text"] = "Server: Welcome " + your_details["name"] + "! Waiting for second player"

            elif msg["command"] == "welcome_second_player":
                your_details["color"] = "Dodgerblue2"
                opponent_details["color"] = "firebrick3"
                if len(msg["updated_board"]) == 0:
                    lbl_status["text"] = "Server: Welcome " + your_details["name"] + "! Game will start soon"

            update_board(msg["updated_board"])




        elif msg["command"] == "opponent_name":
            opponent_details["name"] = msg["opponent_nick"]
            your_details["symbol"] = msg["your_symbol"]

            # set opponent symbol
            if your_details["symbol"] == "X":
                opponent_details["symbol"] = "O"
            else:
                opponent_details["symbol"] = "X"

            lbl_status["text"] = "STATUS: " + opponent_details["name"] + " is connected!"
            sleep(3)
            # is it your turn to play? hey! 'O' comes before 'X'
            if your_details["symbol"] == msg["current_turn"]:
                lbl_status["text"] = "STATUS: Your turn! (" + your_details["symbol"] + ")"
                your_turn = True

            else:
                lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn! (" + opponent_details["symbol"] + ")"
                your_turn = False


        elif msg["command"] == "new_move":
            update_board(msg["updated_board"])

            if msg["current_turn"] == your_details["symbol"]:
                your_turn = True

    client_socket.close()


# def start_the_game(player_id, room_id):
def start_the_game():
    room_id = "60c64517b9f846397cfb66ae"
    player_id = "60c3d0ae531e2ceec167b23a"
    # player_id = "60c3d13127d155fbbdb05592"

    game_data = {"player_id": player_id, "room_id": room_id}
    connect_to_server(game_data)


start_the_game()
window.mainloop()
