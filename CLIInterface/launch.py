#! /usr/bin/env python3

# Launch script to quickly start server and GUI.
# 
# Author: vrusaeva
# Version: v0.8 (11/16/2025)

import time
import traceback
from multiprocessing import freeze_support
import threading
import gui
from server import start_server

freeze_support()

def run():
    server = None
    try:
        server = threading.Thread(target=start_server)
        server.start()
        time.sleep(2)
        if not server.is_alive():
            raise Exception("Server failed to start, exiting...")
        gui.run_gui()
    except Exception:
        traceback.print_exc()
    finally:
        if server and server.is_alive():
            server.join()
        print('All processes finished.')

if __name__ in {"__main__", "__mp_main__"}:
    run()
