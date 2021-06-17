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

board_checked_fields = []
your_turn = False

your_details = {
    "name": "Player1",
    "symbol": "X",
    "color": "",
    "score": 0
}

opponent_details = {
    "name": "Player2",
    "symbol": "O",
    "color": "",
    "score": 0
}

def start_the_game(player_id, room_id):
    #in case is someone go out and come back
    global board_checked_fields, your_turn
    board_checked_fields = []
    your_turn = False

    # MAIN GAME WINDOWma
    window = Tk()
    window.title("Tic-Tac-Toe by Jędrzej Jagiełło")
    content = Frame(window)
    content.grid(row=0, column=0)

    gameInfo = ttk.Frame(content, width=600, height=150)
    gameBoard = ttk.Frame(content, borderwidth=5, relief="ridge", width=450, height=450)
    gamePoints = ttk.Frame(content, borderwidth=5, relief="ridge")
    gameHistory = ttk.Frame(content, borderwidth=5, relief="ridge")

    gameInfo.grid(column=0, row=0, columnspan=2)
    gameBoard.grid(column=0, row=1, rowspan=2)
    gamePoints.grid(column=1, row=1)
    gameHistory.grid(column=1, row=2)


    lbl_status = ttk.Label(gameInfo, text="Status: Not connected to server", font="Helvetica 14 bold")
    lbl_status.grid(row=1, pady="3")

    player_scores = ttk.Label(gamePoints, text="Players scores:\n{}: {}\n{}: {}".format(your_details["name"], "200", opponent_details["name"], "100"), font=('consolas 8'), justify=CENTER)
    player_scores.grid(row=1)

    moves_history = ttk.Label(gameHistory, text="Round history:\n...",font=('consolas 10'), justify=CENTER)
    moves_history.grid(row=1)


    buttonsList = [[], [], []]
    for i in range(3):
        for j in range(3):
            buttonsList[i].append(
                Button(gameBoard, text="   ", width=3, padx=5, bd=5, bg="gold2", font=('arial', 60, 'bold'), relief="sunken"))
            buttonsList[i][j].config(command=lambda row=i, col=j: click(row, col))
            buttonsList[i][j].grid(row=i, column=j)


    def check():  # Checks for victory or Draw
        global your_details
        for i in range(3):
            if (buttonsList[i][0]["text"] == buttonsList[i][1]["text"] == buttonsList[i][2]["text"] ==
                    your_details["symbol"] or buttonsList[0][i]["text"] == buttonsList[1][i]["text"] ==
                    buttonsList[2][i]["text"] == your_details["symbol"]):
                client.send(json.dumps({"command": "game_won", "winner_symbol": your_details["symbol"]}).encode(FORMAT))

        if (buttonsList[0][0]["text"] == buttonsList[1][1]["text"] == buttonsList[2][2]["text"] == your_details[
            "symbol"] or buttonsList[0][2]["text"] == buttonsList[1][1]["text"] == buttonsList[2][0]["text"] ==
                your_details["symbol"]):
            client.send(json.dumps({"command": "game_won", "winner_symbol": your_details["symbol"]}).encode(FORMAT))

        # DRAW
        elif (buttonsList[0][0]["state"] == buttonsList[0][1]["state"] == buttonsList[0][2]["state"] ==
              buttonsList[1][0]["state"] == buttonsList[1][1]["state"] == buttonsList[1][2]["state"] ==
              buttonsList[2][0]["state"] == buttonsList[2][1]["state"] == buttonsList[2][2][
                  "state"] == DISABLED):
            client.send(json.dumps({"command": "draw"}).encode(FORMAT))


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

            moves_history["text"] = moves_history["text"].replace("\n...","")
            moves_history["text"] = moves_history["text"] + "\n{} -> [{},{}]".format(your_details["symbol"], row, col)

            client.send(json.dumps(
                {"command": "new_move", "updated_board": board_checked_fields, "next_turn_symbol": opponent_details["symbol"]}).encode(FORMAT))
            lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn! (" + opponent_details["symbol"] + ")"

            check()


    def update_board(updated_board):
        global your_turn, your_details, board_checked_fields
        if len(updated_board) > len(board_checked_fields):
            board_checked_fields = updated_board


        #update current board and update game history
        moves_history["text"] = "Game history:" if len(updated_board) > 0 else "Game history:\n..."
        for single_move in board_checked_fields:
            color = your_details["color"] if single_move["symbol"] == your_details["symbol"] else opponent_details["color"]
            buttonsList[single_move["row"]][single_move["col"]].config(text=single_move["symbol"], state=DISABLED, disabledforeground=color)
            moves_history["text"] = moves_history["text"] + "\n{} -> [{},{}]".format(single_move["symbol"], single_move["row"], single_move["col"])



    def connect_to_server(game_data):
        global client, PORT, SERVER

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER, PORT))
            client.send(game_data.encode(FORMAT))
            threading._start_new_thread(receive_message_from_server, (client, "m"))


        except Exception as e:
            messagebox.showerror(title="ERROR!!!", message=e)


    def receive_message_from_server(client_socket, m):
        global your_details, opponent_details, your_turn
        while True:
            from_server = client_socket.recv(4096).decode(FORMAT)
            if not from_server: break

            msg = json.loads(from_server)

            if msg["command"].startswith("welcome"):
                your_details["symbol"] = msg["your_symbol"]
                your_details["name"] = msg["your_nick"]
                your_details["score"] = msg["your_score"]

                player_scores["text"] = "Players scores:\n{}: {}".format(your_details["name"], your_details["score"])

                if your_details["symbol"] == "X":
                    opponent_details["symbol"] = "O"
                else:
                    opponent_details["symbol"] = "X"

                if msg["opponent_nick"] != "":
                    opponent_details["name"] = msg["opponent_nick"]
                    opponent_details["score"] = msg["opponent_score"]
                    player_scores["text"] = "Players scores:\n{}: {}\n{}: {}".format(your_details["name"], your_details["score"],
                                                                                     opponent_details["name"], opponent_details["score"])

                # if it's continuation of the game
                if msg["current_turn"] == your_details["symbol"]:
                    if len(msg["updated_board"]) > 0:
                        your_turn = True
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


            #it's turned on only if match is from the start
            elif msg["command"] == "first_game_start":
                lbl_status["text"] = "STATUS: " + opponent_details["name"] + " is connected!"
                sleep(3)

                your_turn = True if msg["current_turn"] == your_details["symbol"] else False

                if your_turn == True:
                    lbl_status["text"] = "STATUS: Your turn! (" + your_details["symbol"] + ")"
                else:
                    lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn! (" + opponent_details["symbol"] + ")"

            elif msg["command"] == "new_move":
                update_board(msg["updated_board"])

                if msg["current_turn"] == your_details["symbol"]:
                    your_turn = True
                    lbl_status["text"] = "STATUS: Your turn! (" + your_details["symbol"] + ")"
                else:
                    lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn! (" + opponent_details["symbol"] + ")"

            elif msg["command"] == "game_won":
                your_turn = False
                lbl_status["text"] = "GAME OVER! {} is the winner!".format(msg["winner_nick"])

                if your_details["name"] == msg["winner_nick"]:
                    lbl_status.config(foreground=your_details["color"])
                else:
                    lbl_status.config(foreground=opponent_details["color"])

            elif msg["command"] == "draw":
                your_turn = False
                lbl_status["text"] = "GAME OVER! It's a DRAW!"
                lbl_status.config(foreground=your_details["color"])

        client_socket.close()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()
            client.send(json.dumps({"command": "!DISCONNECT"}).encode(FORMAT))

    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            return json.JSONEncoder.default(self, o)

    game_data = (JSONEncoder().encode({"player_id": player_id, "room_id": room_id}))
    connect_to_server(game_data)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.resizable(False, False)
    window.mainloop()

#start_the_game()
