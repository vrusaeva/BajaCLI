import socket

# Code for VT Baja interface server.
# 
# Author: vrusaeva
# Version: v0.2 (9/19/2025)

class Network:
    def __init__(self):
        self.HOST = "127.0.0.1"  # localhost
        self.PORT = 60161  
        self.connection = None
        self.address = None
    
    def create_and_listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            self.connection, self.address = s.accept()
            return self.connection, self.address

nw = Network()
connection, address = nw.create_and_listen()

with connection:
    print(address)
    while(True):
        data = connection.recv(1024)
        if not data:
            break
        connection.sendall(data)