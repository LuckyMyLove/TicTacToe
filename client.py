import socket

BUFFER = 1024

# Create a socket instance
clientSocket = socket.socket()

# Using the socket connect to a server...in this case localhost
clientSocket.connect(("localhost", 80))
print("Connected to localhost")

# Send a message to the web server to supply a page as given by Host param of GET request

HTTPMessage = "GET / HTTP/1.1\r\nHost: localhost\r\n Connection: close\r\n\r\n"

bytes = str.encode(HTTPMessage)

clientSocket.sendall(bytes)

# Receive the data

#while (True):

clientSocket.close()