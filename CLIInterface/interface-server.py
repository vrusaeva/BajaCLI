import socket
import selectors
import types

# Code for VT Baja interface server.
# 
# Author: vrusaeva
# Version: v0.2 (9/19/2025)

class Network:
    def __init__(self):
        self.HOST = "127.0.0.1"  # localhost
        self.PORT = 60161  
        self.sel = selectors.DefaultSelector()
        self.ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def create_and_listen(self):
        self.ls.bind((self.HOST, self.PORT)) 
        self.ls.listen()
        self.ls.setblocking(False) # prevent wait/queue when server is not busy
        self.sel.register(self.ls, selectors.EVENT_READ, data = None) # monitor listening socket
    
    def event_loop(self):
        try:
            while True:
                events = self.sel.select(timeout=None) # wait for clients to connect
                for key, mask in events:
                    if key.data is None:
                        self.accept_conn(key.fileobj) # listening socket
                    else:
                        self.run_test(key, mask) # client socket
        except KeyboardInterrupt:
            self.sel.close()
    
    # accept client connections on listening socket
    def accept_conn(self, socket):
        connection, address = socket.accept()
        print(address)
        connection.setblocking(False)
        data = types.SimpleNamespace(addr=address, inp=b"", out=b"") 
        events = selectors.EVENT_READ | selectors.EVENT_WRITE # can communicate two ways with client sockets
        self.sel.register(connection, events=events, data=data)
    
    def run_test(self, key, mask):
        socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            received = socket.recv(1024)
            if received:
                data.out += received # adds data to output queue
            else: # end of test operation
                print("Closing connection")
                self.sel.unregister(socket)
                socket.close()
        if mask & selectors.EVENT_WRITE:
            if data.out:
                print("Echoing")
                sent = socket.send(data.out)
                data.out = data.out[sent:] # removes sent data from output queue


nw = Network()
nw.create_and_listen()
nw.event_loop()


# with connection:
    # print(address)
    # while(True):
        # data = connection.recv(1024)
        # if not data:
            # break
        # connection.sendall(data)