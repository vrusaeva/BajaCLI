import socket
import selectors
import types
import csv
from multiprocessing import Event

# Code for VT Baja interface server.
# Should be able to handle multiple test requests at once, but this is not yet tested.
# 
# Author: vrusaeva
# Version: v0.8 (11/16/2025)

class Network:
    def __init__(self):
        self.HOST = "127.0.0.1"  # localhost
        self.PORT = 60162  
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
                events = self.sel.select(timeout=300) # wait for clients to connect
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
        # data dict usable for all data storage
        data = types.SimpleNamespace(
            addr=address, 
            inp=bytearray(b""), 
            out=bytearray(b""),
            codes=[],
            processed=False
        ) 
        events = selectors.EVENT_READ | selectors.EVENT_WRITE # can communicate two ways with client sockets
        self.sel.register(connection, events=events, data=data)

    def write_one(self, file, data):
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            # encode whole row at once
            data.out.extend(",".join(row).encode('utf-8'))
            data.out.extend(b"\n") # end of line
        data.out.extend(b";") # end of file
    
    def build_output(self, code, data):
        # temporary code for now, should actually communicate with sensors to receive data
        match(code):
            case 'a': # accelerometer
                with open(file = r"C:\Users\vrusa\OneDrive\Documents\BajaCLI\accel_2025-04-02_1.csv", mode = 'r') as file:
                    self.write_one(file, data)
            case 's': # strain (using random file for now)
                with open(file = r"C:\Users\vrusa\OneDrive\Documents\BajaCLI\Trial_9.csv", mode = 'r') as file:
                    self.write_one(file, data)
            case 'b': # bevel
                with open(file = r"C:\Users\vrusa\OneDrive\Documents\BajaCLI\Bevel_75_ft_lbs_1.csv", mode = 'r') as file:
                    self.write_one(file, data)
            case default:
                print("Unsupported code was sent to the server.")
        
    
    def run_test(self, key, mask):
        socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            # flag to prevent reprocessing of same data
            if (data.processed):
                return
            received = socket.recv(1024)
            if received:
                data.inp.extend(received) # adds data to input buffer
                decoded = data.inp.decode() # converts input buffer to string
                # when exit char is sent
                if '#' in decoded:
                    print("Completed receiving")
                    end_index = decoded.index('#')
                    decoded = decoded[:end_index] # strip off any unnecessary last characters
                    data.codes = [code for code in decoded.split(" ") if code.strip()] # make sure no empty strings are used as codes
                    print(f"Number of codes: {len(data.codes)}")
                    # adds output from each CSV file to overall output buffer
                    for code in data.codes:
                        self.build_output(code, data)
                    # exit char when finished building output buffer
                    data.out.extend(b"#")
                    data.processed = True
            else: # end of test operation
                print("Closing connection")
                self.sel.unregister(socket)
                socket.close()
                return
        if mask & selectors.EVENT_WRITE:
            if data.out:
                print("Sending")
                sent = socket.send(data.out) # sends some amount of data bytes, may not send all at once
                data.out = data.out[sent:] # removes sent data from output queue
                return

def start_server():
    nw = Network()
    nw.create_and_listen()
    print("Started server")
    nw.event_loop()