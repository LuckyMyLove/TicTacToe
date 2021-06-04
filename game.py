from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient
import random as random

size_of_board = 600

class singleGame():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic Tac Toe by Jędrzej Jagiełło')
        self.symbol = 'X'
        #self.window.geometry('{}x{}'.format(size_of_board, size_of_board))

        #start from:
        #self.waitingRoom()

    def mainloop(self):
        self.window.mainloop()

    def waitingRoom(self, u1_id, u2_id, room_id):
        cluster = MongoClient('mongodb+srv://dBUser:72qNFNDh5uGIQcrB@maincluster.3mttb.mongodb.net/TicTacToe?retryWrites=true&w=majority')
        db = cluster['TicTacToe']
        self.usersData = db['userData']
        self.gamesData = db['gamesData']
        self.current_room_id = room_id

        #self.current_room_id = self.gamesData.find_one({"_id": room_id})

        self.u1_nick = self.usersData.find_one({"_id": u1_id})["username"]
        if (u2_id != ''):
            self.u2_nick = self.usersData.find_one({"_id": u2_id})["username"]
            self.gamesData.update_one({"_id": self.current_room_id}, {"$set": {"u2_id": u2_id}})
            self.generateEmptyBoard()
        else:
            frame = LabelFrame(self.window, relief="flat")
            frame.pack(expand=True, pady=size_of_board / 3)
            Label(frame, text="Waiting for second player...", font=50, fg="black").pack(pady=5)


    def changePlayer(self):  # Function to change the operand for the next player
        for i in ['O', 'X']:
            if not (i == self.symbol):
                self.symbol = i
                break

    def finish(self):  # Resets the game
        self.gamesData.update_one({"_id": self.current_room_id}, {"$set": {"is_finished": 1}})
        self.window.destroy()

    def check(self):  # Checks for victory or Draw
        for i in range(3):
            if (self.buttonsList[i][0]["text"] == self.buttonsList[i][1]["text"] == self.buttonsList[i][2]["text"] == self.symbol or self.buttonsList[0][i]["text"] == self.buttonsList[1][i]["text"] == self.buttonsList[2][i]["text"] == self.symbol):
                messagebox.showinfo("Congrats!!", "'" + self.symbol + "' has won")
                self.finish()

        if (self.buttonsList[0][0]["text"] == self.buttonsList[1][1]["text"] == self.buttonsList[2][2]["text"] == self.symbol or self.buttonsList[0][2]["text"] == self.buttonsList[1][1]["text"] == self.buttonsList[2][0]["text"] == self.symbol):
            messagebox.showinfo("Congrats!!", "'" + self.symbol + "' has won")
            self.finish()

        #DRAW
        elif (self.buttonsList[0][0]["state"] == self.buttonsList[0][1]["state"] == self.buttonsList[0][2]["state"] == self.buttonsList[1][0]["state"] == self.buttonsList[1][1]["state"] == self.buttonsList[1][2]["state"] ==
              self.buttonsList[2][0]["state"] == self.buttonsList[2][1]["state"] == self.buttonsList[2][2]["state"] == DISABLED):
            messagebox.showinfo("DRAW!", "The match ended in a draw")
            self.finish()

    def generateEmptyBoard(self):
        content = ttk.Frame(self.window)
        content.grid(row=0, column=0)

        self.gameInfo = ttk.Frame(content, width=600, height=150)
        self.gameBoard = ttk.Frame(content, borderwidth=5, relief="ridge", width=450, height=450)
        self.gamePoints = ttk.Frame(content, borderwidth=5, relief="ridge", width=150, height=50)
        self.gameHistory = ttk.Frame(content, borderwidth=5, relief="ridge", width=150, height=150)

        self.gameInfo.grid(column=0, row=0, columnspan=2)
        self.gameBoard.grid(column=0, row=1, rowspan=2)
        self.gamePoints.grid(column=1, row=1)
        self.gameHistory.grid(column=1, row=2)

        #self.chance_label = ttk.Label(self.gameInfo, text=self.symbol + "'s Chance").grid(row=0, pady="3")
        ttk.Label(self.gameInfo,text='{} (X) VS {} (O)'.format(self.u1_nick, self.u2_nick), font=('arial', 15, 'bold')).grid(row=1, pady="3")

        ttk.Label(self.gamePoints, text="Score:").grid(row=1)
        ttk.Label(self.gamePoints, text="{}: {}".format(self.u1_nick, self.usersData.find_one({"username": self.u1_nick})["points"])).grid(row=2)
        ttk.Label(self.gamePoints, text="{}: {}".format(self.u2_nick, self.usersData.find_one({"username": self.u2_nick})["points"])).grid(row=2)

        ttk.Label(self.gameHistory, text="Round history:").grid(row=1)
        ttk.Label(self.gameHistory, text="Player1: 1, 1").grid(row=2)
        ttk.Label(self.gameHistory, text="Player2: 3, 1").grid(row=3)

        self.buttonsList = [[], [], []]
        for i in range(3):
            for j in range(3):
                self.buttonsList[i].append(Button(self.gameBoard, text="   ", width=3, padx=5, bd=5, bg="gold2", font=('arial', 60, 'bold'), relief="sunken"))
                self.buttonsList[i][j].config(command=lambda row=i, col=j: self.click(row, col))
                self.buttonsList[i][j].grid(row=i, column=j)

    def click(self, row, col):
        symbolColour = {'O': "firebrick3", 'X': "Dodgerblue2"}
        self.buttonsList[row][col].config(text=self.symbol, state=DISABLED, disabledforeground=symbolColour[self.symbol])
        self.check()
        self.changePlayer()
        #self.chance_label.config(text=self.symbol + "'s Chance")

def start_the_game(u1_id, u2_id, room_id):
    game_instance = singleGame()
    game_instance.waitingRoom(u1_id, u2_id, room_id)
    game_instance.mainloop()




# def start_the_game(u1_id, u2_id, room_id):
#     cluster = MongoClient('mongodb+srv://dBUser:72qNFNDh5uGIQcrB@maincluster.3mttb.mongodb.net/TicTacToe?retryWrites=true&w=majority')
#     db = cluster['TicTacToe']
#     usersData = db['userData']
#
#     current_room = db['gamesData'].find({"_id": room_id})
#     u1_nick = usersData.find_one({"_id": u1_id})["username"]
#     if(u2_id != ''):
#         u2_nick = usersData.find_one({"_id": u2_id})["username"]
#         game_instance = singleGame()
#         game_instance.mainloop()
#     else:
#         waitng_room = waitingRoom()
#         waitng_room.mainloop()

