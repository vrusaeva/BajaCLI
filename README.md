## BajaCLI
Command-line/graphical interface to run testing on VT Baja SAE vehicles.

## Current Status
Server capable of sending multiple full CSV files to client using sample testing data. GUI up on localhost using NiceGUI.

## Requirements 
- Python 3.11
- NiceGUI >3.1.0

## Usage
1. Clone the repo
2. Configure the ports for the client and server as necessary
3. Start the server (run server.py)
4. Start the GUI (run gui.py) or command-line interface
5. Run some tests! Monitor output on the command line for errors.

TODO:
- Connection to sensors + testing
- Finish GUI (add other screens/better user notification of processes)