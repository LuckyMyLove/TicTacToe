import socket
import sys
from _thread import *

BUFFER = 1024
ip = "127.0.0.1"
port = 80

# Create server socket object
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to port 6869
try:
    socket.bind((ip, port))
except socket.error:
    print('Failed')
    sys.exit()

socket.listen(2)
print("Server is on")

players = []
gameList = []

def runningGame(clientSock):
    clientSock.send("Welcome to Tic Tac Toe")
    # Main connection loop. Handles all messages from client
    while True:
        pass

# Main loop
while True:
    clientSock, addr = socket.accept()
    print('Connected to', addr)

    start_new_thread(runningGame, (clientSock,))

socket.close()
