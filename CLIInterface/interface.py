import json 
import socket

# Simple CLI-based interface to run VT Baja tests.
# 
# Author: vrusaeva
# Version: v0.2 (9/19/2025)
class CLIInterface:
    def __init__(self):
        self.HOST = "127.0.0.1"  # localhost
        self.PORT = 60161
    
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

    def regular_test(self, file, code, connection):
        # Basic echo functionality 
        with connection:
            match(code):
                case "a":
                    connection.sendall(b"accel")
                    print(connection.recv(1024))
                case "s":
                    connection.sendall(b"accel")
                    print(connection.recv(1024))
                case default:
                    print("Not implemented")

    def multi_test(self, file, codes, connection):
        for code in codes:
            self.regular_test(file, code, connection)

    def run_handler(self, in_string, connection):
        inputs = in_string.split()
        if not (inputs[0] == "-f"):
            print("Improperly entered command.")
            return()
        file = open(inputs[1] + ".csv", "w")
        match(inputs[2]):
            case "-t":
                self.regular_test(file, inputs[3], connection)
            case "-tm":
                self.multi_test(file, inputs[3:], connection)
            case default:
                print("Improperly entered command.")

    def json_hander(self, in_string, connection):
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
            file = open(json_dict['filename'] + ".csv", "w")
            if (json_dict['multitest']):
                self.multi_test(file, json_dict['tests'], connection)
            else:
                self.regular_test(file, json_dict['test'], connection)
        except KeyError:
            print("JSON file was not formatted correctly. Please check the example config file.")
        

    def option_selector(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.connect((self.HOST, self.PORT))

            while(True):
                in_string = input(">>")
                if (in_string == "help"):
                    self.help_menu()
                    continue

                if (in_string == "quit"):
                    print("Goodbye.")
                    break

                if (in_string[:4] == "run "):
                    self.run_handler(in_string[4:], connection)
                elif (in_string[:5] == "runc "):
                    self.json_hander(in_string[5:], connection)
                else:
                    print("You did something that caused an error or something that hasn't been implemented yet.")


print("-----------------------\nWelcome to the VT Baja Testing Interface!\n-----------------------\n")

print("Run a test or enter 'help' for help. Enter 'quit' to exit.\n")

interface = CLIInterface()

interface.option_selector()
