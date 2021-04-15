from tkinter import *
from collections import namedtuple

size_of_board = 600
entryWidth = 30


class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic Tac Toe by Jędrzej Jagiełło')
        self.window.geometry('{}x{}'.format(size_of_board, size_of_board))

        self.roomsList = []
        #start from:
        self.loginWindow()

    def mainloop(self):
        self.window.mainloop()

    def loginWindow(self):
        self.loginWindowFrame = LabelFrame(self.window, relief="flat")
        self.loginWindowFrame.pack(expand=True, pady=size_of_board/3)

        Label(self.loginWindowFrame, text="Please insert your nick:", font=30, fg="black").pack(pady=5)
        self.nick = Entry(self.loginWindowFrame, width = entryWidth, borderwidth = 2, relief="ridge", bg="white") #needs to add validation here
        self.nick.pack(pady=(0,5))
        self.loginWindowButton = Button(self.loginWindowFrame, text="Next", width= 10, command=self.lobbyList).pack()

    def lobbyList(self):
        self.loginWindowFrame.pack_forget()

        self.roomsFrame = LabelFrame(self.window, relief="flat", height=100, width=600)
        self.availableRooms = LabelFrame(self.window, relief="flat", height=400, width=600)
        self.createRoomFrame = LabelFrame(self.window, relief="flat", height=100, width=600)

        self.roomsFrame.pack(side=TOP)
        self.availableRooms.pack(side=TOP)
        self.createRoomFrame.pack(side=BOTTOM)

        Label(self.roomsFrame, text="Existing rooms:", font=("Courier", 20), fg="black").pack(side=TOP)

        self.newRoomName = Entry(self.createRoomFrame, width=20, borderwidt=2, relief="ridge", bg="white")  # needs to add validation here

        self.generateRooms()

        self.newRoomName.pack(side=TOP)
        Button(self.createRoomFrame, text="Create new room", width=15, command=self.newRoom, justify="right").pack(
            side=TOP)


    def generateRooms(self):
        for widget in self.availableRooms.winfo_children():
            widget.destroy()

        if len(self.roomsList) > 0:
            for room_number in range(len(self.roomsList)):
                room_text = "#" + str(room_number+1) + " " + self.roomsList[room_number]["room_name"]
                Label(self.availableRooms, text=room_text, font=("Courier", 10), fg="black").pack()

    def newRoom(self):
        self.roomsList.append(
            {"room_name": self.newRoomName.get(), 'places_taken': 0, 'player1_id': 1, 'player2_id': 2, 'moves': []})
        print(self.roomsList)
        self.generateRooms()


game_instance = Tic_Tac_Toe()
game_instance.mainloop()
