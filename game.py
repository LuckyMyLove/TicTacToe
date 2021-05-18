from tkinter import *
from tkinter import ttk

size_of_board = 600



class singleGame():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic Tac Toe by Jędrzej Jagiełło')
        self.window.geometry('{}x{}'.format(size_of_board, size_of_board))
        #start from:
        self.generateEmptyBoard()

    def mainloop(self):
        self.window.mainloop()

    def generateEmptyBoard(self):
        content = ttk.Frame(self.window, width=600, height=600)
        content.grid(row=0, column=0)

        self.gameInfo = ttk.Frame(content, width=600, height=150)
        self.gameBoard = ttk.Frame(content, borderwidth=5, relief="ridge", width=450, height=450)
        self.gameHistory = ttk.Frame(content, borderwidth=5, relief="ridge")

        self.gameInfo.grid(column=0, row=0)
        self.gameBoard.grid(column=0, row=1)
        self.gameHistory.grid(column=1, row=1)

        ttk.Label(self.gameInfo, text="Round 1").grid(row=0, pady="3")
        ttk.Label(self.gameInfo,text="Player1 (X) VS Player2 (O)").grid(row=1, pady="3")
        ttk.Label(self.gameInfo,text="Player1 WIN / DRAW!").grid(row=2, pady="3")
        ttk.Button(self.gameInfo, text="Play again").grid(row=3, pady="3")
        ttk.Button(self.gameInfo, text="Quit").grid(row=4, pady="3")

        ttk.Label(self.gameHistory, text="Score:").grid(row=0, pady="3")
        ttk.Label(self.gameHistory, text="Player1: 100").grid(row=1, pady="3")
        ttk.Label(self.gameHistory, text="Player2: 300").grid(row=2, pady="3")
        ttk.Label(self.gameHistory, text="Round history:").grid(row=3, pady="5")
        ttk.Label(self.gameHistory, text="Player1: 1, 1").grid(row=4, pady="2")
        ttk.Label(self.gameHistory, text="Player2: 3, 1").grid(row=5, pady="2")




        # self.self.gameHistory = LabelFrame(self.window, relief="flat", height=100, width=600, bg="yellow")
        # self.gameBoard = LabelFrame(self.window, relief="flat", height=500, width=400, bg="blue")
        # self.self.gameHistory = LabelFrame(self.self.gameHistory, relief="flat", height=500, width=100, bg="red")
        #
        # self.self.gameHistory.pack(side=TOP)
        # self.gameBoard.pack(side=LEFT)
        # self.self.gameHistory.pack(side=RIGHT)
        #
        # Label(self.self.gameHistory, text="Jebać pis", font=("Courier", 20), fg="black").pack(side=TOP)
        # for i in range(3):
        #     for j in range(3):
        #         text = "Player1: [{}][{}]".format(i, j)
        #         Label(self.self.gameHistory, text=text, font=("Courier", 10), fg="black").pack(side=TOP)



game_instance = singleGame()
game_instance.mainloop()
