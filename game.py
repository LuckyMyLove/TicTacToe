from tkinter import *
from tkinter import ttk, messagebox
import random as random

size_of_board = 600

class singleGame():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic Tac Toe by Jędrzej Jagiełło')
        self.symbol = 'X'
        #self.window.geometry('{}x{}'.format(size_of_board, size_of_board))
        #start from:
        self.generateEmptyBoard()

    def mainloop(self):
        self.window.mainloop()

    def changePlayer(self):  # Function to change the operand for the next player
        for i in ['O', 'X']:
            if not (i == self.symbol):
                self.symbol = i
                break

    def reset(self):  # Resets the game
        for i in range(3):
            for j in range(3):
                self.buttonsList[i][j]["text"] = " "
                self.buttonsList[i][j]["state"] = NORMAL
        #self.symbol = random.choice(['O', 'X'])

    def check(self):  # Checks for victory or Draw
        for i in range(3):
            if (self.buttonsList[i][0]["text"] == self.buttonsList[i][1]["text"] == self.buttonsList[i][2]["text"] == self.symbol or self.buttonsList[0][i]["text"] == self.buttonsList[1][i]["text"] == self.buttonsList[2][i]["text"] == self.symbol):
                messagebox.showinfo("Congrats!!", "'" + self.symbol + "' has won")
                self.reset()

        if (self.buttonsList[0][0]["text"] == self.buttonsList[1][1]["text"] == self.buttonsList[2][2]["text"] == self.symbol or self.buttonsList[0][2]["text"] == self.buttonsList[1][1]["text"] == self.buttonsList[2][0]["text"] == self.symbol):
            messagebox.showinfo("Congrats!!", "'" + self.symbol + "' has won")
            self.reset()

        #DRAW
        elif (self.buttonsList[0][0]["state"] == self.buttonsList[0][1]["state"] == self.buttonsList[0][2]["state"] == self.buttonsList[1][0]["state"] == self.buttonsList[1][1]["state"] == self.buttonsList[1][2]["state"] ==
              self.buttonsList[2][0]["state"] == self.buttonsList[2][1]["state"] == self.buttonsList[2][2]["state"] == DISABLED):
            messagebox.showinfo("Tied!!", "The match ended in a draw")
            self.reset()

    def generateButton(self, container):  # Function to define a button
        singleButton = Button(container, text="   ", width=3, padx=5, bd=5, bg="gold2", font=('arial', 60, 'bold'), relief="sunken")
        return singleButton

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

        ttk.Label(self.gameInfo, text="Round 1").grid(row=0, pady="3")
        ttk.Label(self.gameInfo,text="Player1 (X) VS Player2 (O)").grid(row=1, pady="3")
        ttk.Label(self.gameInfo,text="Player1 WIN / DRAW!").grid(row=2, pady="3")
        ttk.Button(self.gameInfo, text="Play again").grid(row=3, pady="3")
        ttk.Button(self.gameInfo, text="Quit").grid(row=4, pady="3")

        ttk.Label(self.gamePoints, text="Score:").grid(row=1)
        ttk.Label(self.gamePoints, text="Player1: 100").grid(row=2)
        ttk.Label(self.gamePoints, text="Player2: 300").grid(row=3)

        ttk.Label(self.gameHistory, text="Round history:").grid(row=1)
        ttk.Label(self.gameHistory, text="Player1: 1, 1").grid(row=2)
        ttk.Label(self.gameHistory, text="Player2: 3, 1").grid(row=3)

        self.buttonsList = [[], [], []]
        for i in range(3):
            for j in range(3):
                pass
                self.buttonsList[i].append(self.generateButton(self.gameBoard))
                self.buttonsList[i][j].config(command=lambda row=i, col=j: self.click(row, col))
                self.buttonsList[i][j].grid(row=i, column=j)


    def click(self, row, col):
        symbolColour = {'O': "firebrick3", 'X': "Dodgerblue2"}
        self.buttonsList[row][col].config(text=self.symbol, state=DISABLED, disabledforeground=symbolColour[self.symbol])
        self.check()
        self.changePlayer()
        # label.config(text=self.symbol + "'s Chance")

game_instance = singleGame()
game_instance.mainloop()
