import json 
import socket
import selectors
import types
import csv

# Simple CLI-based interface to run VT Baja tests.
# 
# Author: vrusaeva
# Version: v0.2 (9/19/2025)
class CLIInterface:
    def __init__(self):
        self.HOST = "127.0.0.1"  # localhost
        self.PORT = 60161
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel = selectors.DefaultSelector()
    
    def take_input():
        in_string = input(">>")
        return in_string

    def help_menu(self):
        print("To run, use: run -f [CSV file name] -t [test code] -tm [multiple space separated test codes]\n")
        print("To run from a JSON config fie, use: runc -f [config file name]")
        print("Note: DO NOT add .csv or .json to the filename. Please only enter either -t or -tm.\n")
        print("Test codes: \n" \
        "- a = accelerometer test\n" \
        "- s = strain gauge test\n" \
        "More to be added later\n")
        print("Example run command: run -f accel -t a")
        print("Example run command for multiple tests: run -f multi -tm a s")
        print("Example run from JSON: runc -f config")

    def open_connection(self, code, connection):
        connection.setblocking(False)
        connection.connect_ex((self.HOST, self.PORT)) # suppress errors

        data = types.SimpleNamespace(
            id = 0,
            message = code,
            received = [],
            out = code.encode('utf-8'),
        )

        self.sel.register(connection, events=self.events, data=data)
        return connection, data

    def process_connection(self, key, mask):
        socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            received = socket.recv(1024)
            if received:
                data.received.append(received.decode()) # gets received data
                print(f"Received from server: {received.decode()}")
            else: # server closed connection
                print("Server closed this connection")
                self.sel.unregister(socket)
                socket.close()
                return
        if mask & selectors.EVENT_WRITE:
            if data.out:
                print("Sending")
                sent = socket.send(data.out)
                data.out = data.out[sent:] # removes sent data from output queue
        return data
        

    def regular_test(self, file, code):
        # Basic echo functionality 
        # Open a new connection for each test
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection, data = self.open_connection(code, connection)

        # event loop - should only run once per test, but timeout is set to 10 to allow for some buffer
        timeout_count = 0
        max_timeout = 10
        
        while timeout_count < max_timeout:
            events = self.sel.select(timeout=1)
            if not events:
                timeout_count += 1
                continue
                
            for key, mask in events:
                data = self.process_connection(key, mask)
                
                
            # when finished processing
            if not data.out and data.received:
                print("Processed")
                break
        
        if data.received:
            with open(file=file, mode='w', newline='') as csvfile:
                print(data.received)
                writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for message in data.received:
                    writer.writerow([message])
                


    def multi_test(self, file, codes):
        for code in codes:
            self.regular_test(file, code)


    def run_handler(self, in_string):
        inputs = in_string.split()
        if not (inputs[0] == "-f"):
            print("Improperly entered command.")
            return()
        file = inputs[1] + ".csv"
        match(inputs[2]):
            case "-t":
                self.regular_test(file, inputs[3])
            case "-tm":
                self.multi_test(file, inputs[3:])
            case default:
                print("Improperly entered command.")


    def json_hander(self, in_string):
        inputs = in_string.split()
        json_dict = None

        if not (inputs[0] == "-f"):
            print("Improperly entered command.")
            return()
        
        try:
            with open(inputs[1] + '.json', 'r') as file:
                json_dict = json.load(file)
        except FileNotFoundError:
            print("Incorrect filename or file does not exist.")
            return()
        
        try:
            file = json_dict['filename'] + ".csv"
            if (json_dict['multitest']):
                self.multi_test(file, json_dict['tests'])
            else:
                self.regular_test(file, json_dict['test'])
        except KeyError:
            print("JSON file was not formatted correctly. Please check the example config file.")
        

    def option_selector(self):
        while(True):
            in_string = input(">>")
            if (in_string == "help"):
                self.help_menu()
                continue

            if (in_string == "quit"):
                print("Goodbye.")
                break

            if (in_string[:4] == "run "):
                self.run_handler(in_string[4:])
            elif (in_string[:5] == "runc "):
                self.json_hander(in_string[5:])
            else:
                print("You did something that caused an error or something that hasn't been implemented yet.")


print("-----------------------\nWelcome to the VT Baja Testing Interface!\n-----------------------\n")

print("Run a test or enter 'help' for help. Enter 'quit' to exit.\n")

interface = CLIInterface()

interface.option_selector()
