from tkinter import *

size_of_board = 600
entryWidth = 30

class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic Tac Toe by Jędrzej Jagiełło')
        self.window.geometry('%dx%d'%(size_of_board,size_of_board))

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

        print('Provided nick is: %s'% self.nick.get())

        self.roomsFrame = LabelFrame(self.window, relief="flat", bg="black").pack(padx = (0,5))
        self.createRoomFrame = LabelFrame(self.window, relief="flat").pack()

        Label(self.roomsFrame, text="Existing rooms:", font=30, fg="black").pack()
        Button(self.createRoomFrame, text="Create new room", width= 15, command=self.newRoom).pack()

    def newRoom(self):
        pass





game_instance = Tic_Tac_Toe()
game_instance.mainloop()

