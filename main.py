from game import *

size_of_board = 600
entry_width = 30


class Tic_Tac_Toe():
    def __init__(self):
        cluster = MongoClient('mongodb+srv://dBUser:72qNFNDh5uGIQcrB@maincluster.3mttb.mongodb.net/TicTacToe?retryWrites=true&w=majority')
        db = cluster['TicTacToe']
        self.users_data = db['userData']
        self.game_data = db['gamesData']

        self.window = Tk()
        self.window.title('Tic Tac Toe by Jędrzej Jagiełło')
        self.window.geometry('{}x{}'.format(size_of_board, size_of_board))

        self.rooms_list = self.game_data.find()
        # start from:
        self.login_window()

    def mainloop(self):
        self.window.mainloop()

    def login_window(self):
        self.login_window_frame = LabelFrame(self.window, relief="flat")
        self.login_window_frame.pack(expand=True, pady=size_of_board / 3)

        Label(self.login_window_frame, text="Please insert your nick:", font=30, fg="black").pack(pady=5)
        self.nick = Entry(self.login_window_frame, width=entry_width, borderwidth=2, relief="ridge", bg="white")
        self.nick.pack(pady=(0, 5))
        Button(self.login_window_frame, text="Next", width=10, command=lambda: self.try_login()).pack()

    def try_login(self):
        # if we already have provided nick in db, throw error
        if self.users_data.find_one({"username": self.nick.get()}):
            messagebox.showinfo('Duplicate nick', 'There already is nick like this in DB, please provide another one.')
        elif self.nick.get() == '' or str(self.nick.get()).isspace():
            messagebox.showinfo('Error', "Please add nick which won't be only from whitespaces.")
        else:
            new_user = {"username": self.nick.get(), "points": 0}
            self.users_data.insert_one(new_user)
            self.lobby_list()

    def lobby_list(self):
        self.login_window_frame.pack_forget()

        self.rooms_frame = LabelFrame(self.window, relief="flat", height=100, width=600)
        self.available_rooms = LabelFrame(self.window, relief="flat", height=400, width=600)
        self.create_room_frame = LabelFrame(self.window, relief="flat", height=100, width=600)

        self.rooms_frame.pack(side=TOP)
        self.available_rooms.pack(side=TOP)
        self.create_room_frame.pack(side=BOTTOM)

        Label(self.rooms_frame, text="Existing rooms:", font=("Courier", 20), fg="black").pack(side=TOP)
        Button(self.create_room_frame, text="Refresh rooms", width=15, command=lambda: self.generate_rooms(), justify="right").pack(
            side=TOP)

        self.new_room_name = Entry(self.create_room_frame, width=20, borderwidth=2, relief="ridge", bg="white")

        self.generate_rooms()

        self.new_room_name.pack(side=TOP)
        Button(self.create_room_frame, text="Create new room", width=15, command=lambda: self.new_room(), justify="right").pack(
            side=TOP)

    def enter_room(self, room_id):
        current_room = self.game_data.find_one({"_id": room_id})
        current_user_id = self.users_data.find_one({"username": self.nick.get()})["_id"]

        u1_id = current_room["u1_id"]
        u1_nick = self.users_data.find_one({"_id": u1_id})["username"]

        if self.nick.get() == u1_nick:
            start_the_game(current_user_id, '', room_id)
        else:
            self.game_data.update_one({"_id": "room_id"}, {"$set": {"id_u2": current_user_id}})
            start_the_game(u1_id, current_user_id, room_id)

    def generate_rooms(self):
        self.rooms_list = self.game_data.find()

        for widget in self.available_rooms.winfo_children():
            widget.destroy()

        for room in self.rooms_list:
            room_creator = self.users_data.find_one({'_id': room["u1_id"]})["username"]

            if room_creator == self.nick.get():
                room_text = str("# " + room["room_name"] + " / created by: YOU")
                Button(self.available_rooms, text=room_text, font=("Courier", 10), fg="dark orchid",
                       command=lambda room_id=room['_id']: self.enter_room(room_id)).pack()

            else:
                room_text = str("# " + room["room_name"] + " / created by: " + room_creator)
                Button(self.available_rooms, text=room_text, font=("Courier", 10), fg="black",
                       command=lambda room_id=room['_id']: self.enter_room(room_id)).pack()

    def new_room(self):
        if self.game_data.find_one({"room_name": self.new_room_name.get()}):
            messagebox.showinfo('Duplicate room name', "There is already room with name like this in DB, please provide another one.")
        elif self.new_room_name.get() == '' or str(self.new_room_name.get()).isspace():
            messagebox.showinfo('Error', "Please add room name which won't be only from whitespaces.")
        else:
            new_room = {"u1_id": self.users_data.find_one({"username": self.nick.get()})["_id"], "u2_id": "",
                        "room_name": self.new_room_name.get(), "symbol_u1": "X", "symbol_u2": "O", "moves": [], "result": 0}
            self.game_data.insert_one(new_room)
            self.generate_rooms()
            self.enter_room(self.game_data.find_one({"u1_id": new_room["u1_id"]})["_id"])


game_instance = Tic_Tac_Toe()
game_instance.mainloop()
