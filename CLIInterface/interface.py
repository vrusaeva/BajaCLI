import json 
import socket
import selectors
import types
import csv
import traceback

# Simple CLI-based interface to run VT Baja tests.
# 
# Author: vrusaeva
# Version: v0.5 (10/18/2025)
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
        print("To run, use: run -f [one or more CSV filepaths] -t [one or more space separated test codes] \n")
        print("For JSON options, please refer to the example config.json. To run from a JSON config fie, use: runc -f [config file name]")
        print("Note: In this version, please add .csv and .json to all filenames.\n")
        print("Test codes: \n" \
        "- a = accelerometer test\n" \
        "- s = strain gauge test\n" \
        "More to be added later\n")
        print(r"Example run command: run -f C:\Users\<your username>\OneDrive\Documents\BajaCLI\accel -t a")
        print(r"Example run command for multiple tests: run -f C:\Users\<your username>\OneDrive\Documents\BajaCLI\accel.csv C:\Users\<your username>\OneDrive\Documents\BajaCLI\othertest.csv -tm a s")
        print(r"Example run from JSON: runc -f C:\Users\<your username>\OneDrive\Documents\BajaCLI\config.json")

    def open_connection(self, codes, connection):
        connection.setblocking(False)
        connection.connect_ex((self.HOST, self.PORT)) # suppress errors
        # data dict usable for all types of data storage
        data = types.SimpleNamespace(
            out = bytearray(b""),
            received = bytearray(b""),
            files = []
        )
        # adds all codes to output buffer
        for code in codes:
            data.out.extend((code + " ").encode("utf-8"))
        # adds exit character
        data.out.extend(b"#")

        # registers connection to selector
        self.sel.register(connection, events=self.events, data=data)
        return connection, data

    def process_connection(self, key, mask):
        socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            received = socket.recv(1024)
            if received:
                data.received.extend(received) # gets received data
                decoded = data.received.decode()
                # when exit char is sent
                if '#' in decoded:
                    print("Completed receiving")
                    end_index = decoded.index('#')
                    decoded = decoded[:end_index] # split off any unnecessary last chars
                    data.files = [file for file in decoded.split(';') if file.strip()] # make sure no empty strings are processed to files
                    print(f"Processed {len(data.files)} datasets")
                    # prevent reprocessing of data
                    data.received.clear()
            else: # server closed connection
                print("Server closed this connection")
                self.sel.unregister(socket)
                socket.close()
                return
        if mask & selectors.EVENT_WRITE:
            if data.out:
                print("Sending")
                sent = socket.send(data.out)
                data.out = data.out[sent:]
        

    def write(self, rcv_file, file):
        if rcv_file:
            rows = [row for row in rcv_file.split(r'\n') if row.strip()]
            with open(file=file, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in rows:
                    writer.writerow([el for el in row.split(',')])
    

    def test(self, files, codes):
        # change codes to list if not already
        if isinstance(codes, str):
            codes = [codes]

        # open single connection to process all tests
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection, data = self.open_connection(codes, connection)

        # event loop - should only run once per test, but timeout is set to 10 to allow for some buffer
        timeout_count = 0
        max_timeout = 10
        
        while timeout_count < max_timeout:
            events = self.sel.select(timeout=1)
            if not events:
                timeout_count += 1
                continue
                
            for key, mask in events:
                self.process_connection(key, mask)     
                
            # when finished processing
            if not data.out and data.files:
                print("Processed")
                break

        self.sel.unregister(connection)
        connection.close()

        if (len(data.files) != len(files)):
            print("WARNING: Server did not send back data for all requests. There may be a mismatch in data.")
            print("We recommend rerunning your request. If the issue persists, please contact support.")
        print(f"Expected files: {len(files)}, Received datasets: {len(data.files)}")

        for rcv_file, w_file in zip(data.files, files):
            print(f"Writing file {w_file}, data length: {len(rcv_file)}")
            self.write(rcv_file, w_file)
                

    def run_handler(self, in_string):
        try:
            inputs = in_string.split()
            if not (inputs[0] == "-f"):
                print("Improperly entered command.")
                return()
            index = inputs.index("-t")
            files = inputs[1 : index]
            self.test(files, inputs[index + 1:])
        except Exception:
            print("Unexpected error in parsing command: ")
            traceback.print_exc()


    def json_hander(self, in_string):
        inputs = in_string.split()
        json_dict = None

        if not (inputs[0] == "-f"):
            print("Improperly entered command.")
            return()
        
        try:
            with open(inputs[1], 'r') as file:
                json_dict = json.load(file)
        except FileNotFoundError:
            print("Incorrect filename or file does not exist.")
            return()
        
        try:
            files = [file for file in json_dict['filename']]
            if (json_dict['multitest']):
                self.test(files, json_dict['tests'])
            else:
                self.test(files, json_dict['test'])
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
