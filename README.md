## BajaCLI
Command-line/graphical interface to run testing on VT Baja SAE vehicles.

## Current Status
Server capable of sending and receiving data on localhost and on remote. GUI up on localhost using NiceGUI. Files can be run on Windows machines using the dist .exe.

## Requirements 
- Python 3.11
- NiceGUI >3.1.0

## Usage
1. Clone the repo.
2. Copy .env.example into a new .env file and update it with your filepaths, your host, and your port if necessary.
3. Run the launch.py script OR on Windows: run launch.exe in the dist folder to start the server and GUI.
4. Run some tests! Monitor output on the command line for errors.

## Usage (Remote)
1. Clone the repo to both your computer and remote (Raspberry Pi).
2. On your computer, copy .env.example into a new .env file and update it with your REMOTE host and port (as well as your desired output folder).
3. On remote host, copy .env.example into a new .env file and update it with your REMOTE host and port (as well as your input folder).
4. Start the server on your remote host by running `python -c "import server; server.start_server()"` from inside the CLIInterface folder.
5. Start the GUI on your computer by running `python gui.py` from inside the CLIInterface folder.
5. Run some tests! Monitor output on the command line for errors.

## TODO
- Connection to sensors + testing
- Finish GUI (add other screens/better user notification of processes)