## BajaCLI
Command-line/graphical interface to run testing on VT Baja SAE vehicles.

## Current Status
Server capable of sending and receiving data on localhost. GUI up on localhost using NiceGUI. Files can be run on Windows machines using the dist .exe.

## Requirements 
- Python 3.11
- NiceGUI >3.1.0

## Usage
1. Clone the repo
2. Configure the ports for the client and server as necessary
3. Run the launch.py script OR on Windows: run launch.exe in the dist folder to start the server and GUI.
4. Run some tests! Monitor output on the command line for errors.

## TODO
- Connection to sensors + testing
- Finish GUI (add other screens/better user notification of processes)