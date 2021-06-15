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
num_cols = 3
your_turn = False
you_started = False


your_details = {
    "name": "Charles",
    "symbol": "X",
    "color" : "",
    "score" : 0
}

opponent_details = {
    "name": " ",
    "symbol": "O",
    "color": "",
    "score": 0
}


# MAIN GAME WINDOW
window = Tk()
window.title("Tic-Tac-Toe Client")
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
#ttk.Label(gameInfo, text='{} (X) VS {} (O)'.format(u1_nick, u2_nick), font=('arial', 15, 'bold')).grid(row=1, pady="3")
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
    buttonsList[row][col].config(text=your_details["symbol"], state=DISABLED, disabledforeground=your_details["color"])
    # check()  # wysłanie informacji na server
    # changePlayer()
    # self.chance_label.config(text=self.symbol + "'s Chance")

def connect_to_server(game_data):
    global client, PORT, SERVER
    game_data = json.dumps(game_data)

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client.send(game_data.encode(FORMAT))  # Send name to server after connecting
        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
        #top_frame.pack(side=TOP)
        #window.title("Tic-Tac-Toe Client - " + game_data["player_id"])
        window.title("Tic-Tac-Toe Client")


    except Exception as e:
        messagebox.showerror(title="ERROR!!!", message=e)
        # tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + SERVER + " on port: " + str(
        #     PORT) + " Server may be Unavailable. Try again later")


def init(arg0, arg1):
    global list_labels, your_turn, your_details, opponent_details, you_started

    sleep(3)

    for i in range(len(list_labels)):
        list_labels[i]["symbol"] = ""
        list_labels[i]["ticked"] = False
        list_labels[i]["label"]["text"] = ""
        list_labels[i]["label"].config(foreground="black", highlightbackground="grey",
                                       highlightcolor="grey", highlightthickness=1)

    lbl_status.config(foreground="black")
    lbl_status["text"] = "STATUS: Game's starting."
    sleep(1)
    lbl_status["text"] = "STATUS: Game's starting.."
    sleep(1)
    lbl_status["text"] = "STATUS: Game's starting..."
    sleep(1)

    if you_started:
        you_started = False
        your_turn = False
        lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn!"
    else:
        you_started = True
        your_turn = True
        lbl_status["text"] = "STATUS: Your turn!"

def receive_message_from_server(client_socket, m):
    global your_details, opponent_details, your_turn, you_started
    while True:
        from_server = client_socket.recv(4096).decode(FORMAT)
        print(from_server)
        if not from_server: break
        #tutaj mniej wiecej skonczyłem
        if from_server.startswith("welcome"):
            if from_server == "welcome_first_player":
                your_details["color"] = "firebrick3"
                opponent_details["color"] = "Dodgerblue2"
                lbl_status["text"] = "Server: Welcome " + your_details["name"] + "! Waiting for second player"

            elif from_server == "welcome_second_player":
                lbl_status["text"] = "Server: Welcome " + your_details["name"] + "! Game will start soon"
                your_details["color"] = "Dodgerblue2"
                opponent_details["color"] = "firebrick3"

        elif from_server.startswith("opponent_name$"):
            temp = from_server.replace("opponent_name$", "")
            temp = temp.replace("symbol", "")
            name_index = temp.find("$")
            symbol_index = temp.rfind("$")
            opponent_details["name"] = temp[0:name_index]
            your_details["symbol"] = temp[symbol_index:len(temp)]

            # set opponent symbol
            if your_details["symbol"] == "X":
                opponent_details["symbol"] = "O"
            else:
                opponent_details["symbol"] = "X"

            lbl_status["text"] = "STATUS: " + opponent_details["name"] + " is connected!"
            sleep(3)
            # is it your turn to play? hey! 'O' comes before 'X'
            if your_details["symbol"] == "X":
                lbl_status["text"] = "STATUS: Your turn!"
                your_turn = True
                you_started = True
            else:
                lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn!"
                you_started = False
                your_turn = False

        elif from_server.startswith("$xy$"):
            temp = from_server.replace("$xy$", "")
            _x = temp[0:temp.find("$")]
            _y = temp[temp.find("$") + 1:len(temp)]

            # update board
            label_index = int(_x) * num_cols + int(_y)
            label = list_labels[label_index]
            label["symbol"] = opponent_details["symbol"]
            label["label"]["text"] = opponent_details["symbol"]
            label["label"].config(foreground=opponent_details["color"])
            label["ticked"] = True

            # Does this cordinate leads to a win or a draw
            result = game_logic()
            if result[0] is True and result[1] != "":  # opponent win
                opponent_details["score"] = opponent_details["score"] + 1
                if result[1] == opponent_details["symbol"]:  #
                    lbl_status["text"] = "Game over, You Lost! You(" + str(your_details["score"]) + ") - " \
                        "" + opponent_details["name"] + "(" + str(opponent_details["score"]) + ")"
                    lbl_status.config(foreground="red")
                    threading._start_new_thread(init, ("", ""))
            elif result[0] is True and result[1] == "":  # a draw
                lbl_status["text"] = "Game over, Draw! You(" + str(your_details["score"]) + ") - " \
                    "" + opponent_details["name"] + "(" + str(opponent_details["score"]) + ")"
                lbl_status.config(foreground="blue")
                threading._start_new_thread(init, ("", ""))
            else:
                your_turn = True
                lbl_status["text"] = "STATUS: Your turn!"
                lbl_status.config(foreground="black")

    client_socket.close()


def get_cordinate(xy):
    global client, your_turn
    # convert 2D to 1D cordinate i.e. index = x * num_cols + y
    label_index = xy[0] * num_cols + xy[1]
    label = list_labels[label_index]

    if your_turn:
        if label["ticked"] is False:
            label["label"].config(foreground=your_details["color"])
            label["label"]["text"] = your_details["symbol"]
            label["ticked"] = True
            label["symbol"] = your_details["symbol"]
            # send xy cordinate to server
            client.send(("$xy$" + str(xy[0]) + "$" + str(xy[1])).encode(FORMAT))
            your_turn = False

            # Does this play leads to a win or a draw
            result = game_logic()
            if result[0] is True and result[1] != "":  # a win
                your_details["score"] = your_details["score"] + 1
                lbl_status["text"] = "Game over, You won! You(" + str(your_details["score"]) + ") - " \
                    "" + opponent_details["name"] + "(" + str(opponent_details["score"])+")"
                lbl_status.config(foreground="green")
                threading._start_new_thread(init, ("", ""))

            elif result[0] is True and result[1] == "":  # a draw
                lbl_status["text"] = "Game over, Draw! You(" + str(your_details["score"]) + ") - " \
                    "" + opponent_details["name"] + "(" + str(opponent_details["score"]) + ")"
                lbl_status.config(foreground="blue")
                threading._start_new_thread(init, ("", ""))

            else:
                lbl_status["text"] = "STATUS: " + opponent_details["name"] + "'s turn!"
    else:
        lbl_status["text"] = "STATUS: Wait for your turn!"
        lbl_status.config(foreground="red")

        # send xy coordinate to server to server

def check_row():
    list_symbols = []
    list_labels_temp = []
    winner = False
    win_symbol = ""
    for i in range(len(list_labels)):
        list_symbols.append(list_labels[i]["symbol"])
        list_labels_temp.append(list_labels[i])
        if (i + 1) % 3 == 0:
            if (list_symbols[0] == list_symbols[1] == list_symbols[2]):
                if list_symbols[0] != "":
                    winner = True
                    win_symbol = list_symbols[0]

                    list_labels_temp[0]["label"].config(foreground="green", highlightbackground="green",
                                                        highlightcolor="green", highlightthickness=2)
                    list_labels_temp[1]["label"].config(foreground="green", highlightbackground="green",
                                                        highlightcolor="green", highlightthickness=2)
                    list_labels_temp[2]["label"].config(foreground="green", highlightbackground="green",
                                                        highlightcolor="green", highlightthickness=2)

            list_symbols = []
            list_labels_temp = []

    return [winner, win_symbol]


# [(0,0) -> (1,0) -> (2,0)], [(0,1) -> (1,1) -> (2,1)], [(0,2), (1,2), (2,2)]
def check_col():
    winner = False
    win_symbol = ""
    for i in range(num_cols):
        if list_labels[i]["symbol"] == list_labels[i + num_cols]["symbol"] == list_labels[i + num_cols + num_cols][
            "symbol"]:
            if list_labels[i]["symbol"] != "":
                winner = True
                win_symbol = list_labels[i]["symbol"]

                list_labels[i]["label"].config(foreground="green", highlightbackground="green",
                                               highlightcolor="green", highlightthickness=2)
                list_labels[i + num_cols]["label"].config(foreground="green", highlightbackground="green",
                                                          highlightcolor="green", highlightthickness=2)
                list_labels[i + num_cols + num_cols]["label"].config(foreground="green", highlightbackground="green",
                                                                     highlightcolor="green", highlightthickness=2)

    return [winner, win_symbol]


def check_diagonal():
    winner = False
    win_symbol = ""
    i = 0
    j = 2

    # top-left to bottom-right diagonal (0, 0) -> (1,1) -> (2, 2)
    a = list_labels[i]["symbol"]
    b = list_labels[i + (num_cols + 1)]["symbol"]
    c = list_labels[(num_cols + num_cols) + (i + 1)]["symbol"]
    if list_labels[i]["symbol"] == list_labels[i + (num_cols + 1)]["symbol"] == \
            list_labels[(num_cols + num_cols) + (i + 2)]["symbol"]:
        if list_labels[i]["symbol"] != "":
            winner = True
            win_symbol = list_labels[i]["symbol"]

            list_labels[i]["label"].config(foreground="green", highlightbackground="green",
                                           highlightcolor="green", highlightthickness=2)

            list_labels[i + (num_cols + 1)]["label"].config(foreground="green", highlightbackground="green",
                                                            highlightcolor="green", highlightthickness=2)
            list_labels[(num_cols + num_cols) + (i + 2)]["label"].config(foreground="green",
                                                                         highlightbackground="green",
                                                                         highlightcolor="green", highlightthickness=2)

    # top-right to bottom-left diagonal (0, 0) -> (1,1) -> (2, 2)
    elif list_labels[j]["symbol"] == list_labels[j + (num_cols - 1)]["symbol"] == list_labels[j + (num_cols + 1)][
        "symbol"]:
        if list_labels[j]["symbol"] != "":
            winner = True
            win_symbol = list_labels[j]["symbol"]

            list_labels[j]["label"].config(foreground="green", highlightbackground="green",
                                           highlightcolor="green", highlightthickness=2)
            list_labels[j + (num_cols - 1)]["label"].config(foreground="green", highlightbackground="green",
                                                            highlightcolor="green", highlightthickness=2)
            list_labels[j + (num_cols + 1)]["label"].config(foreground="green", highlightbackground="green",
                                                            highlightcolor="green", highlightthickness=2)
    else:
        winner = False

    return [winner, win_symbol]


# it's a draw if grid is filled
def check_draw():
    for i in range(len(list_labels)):
        if list_labels[i]["ticked"] is False:
            return [False, ""]
    return [True, ""]

def game_logic():
    result = check_row()
    if result[0]:
        return result

    result = check_col()
    if result[0]:
        return result

    result = check_diagonal()
    if result[0]:
        return result

    result = check_draw()
    return result

#def start_the_game(player_id, room_id):
def start_the_game():
    room_id = "60c64517b9f846397cfb66ae"
    player_id = "60c3d0ae531e2ceec167b23a"
    #u2_id = ""
    #player_id = "60c3d13127d155fbbdb05592"

    game_data = {"player_id": player_id, "room_id": room_id}
    connect_to_server(game_data)

start_the_game()
window.mainloop()