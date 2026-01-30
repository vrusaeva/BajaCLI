from nicegui import ui, app
import asyncio
import interface
import traceback
import sys, os
from dotenv import load_dotenv

# GUI to interact with Baja CLI interface.
# 
# Author: vrusaeva
# Version: v0.8 (11/16/2025)

VERSION = '0.8'
width = 0
height = 0

sensors_active = []
ac_codes = []
valid_codes_dict = {"Accel": 'a', "Strain": 's', "Bevel": 'b'}

boxes = []
json_field = None
output_field = None
firstrun = True

client = interface.CLIInterface()

def get_asset_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, '../assets')
    else:
        return os.path.join(os.path.dirname(__file__), '../assets')

app.add_static_files('/static-assets', get_asset_path())

class Splash(ui.element):
    def __init__(self):
        super().__init__(tag='div')
        self.style('position: fixed; display: block; width: 100%; height: 100%;'
                   'top: 0; left: 0; right: 0; bottom: 0; z-index: 2; cursor: pointer;'
                   'background-color:' + f'rgba{(134, 31, 65, 0.75)};')        
        with self:
            with ui.element('div').classes("h-screen flex items-center justify-center"):
                ui.image('/static-assets/splash_image.png').classes('h-auto max-w-4xl rounded-lg flex justify-center')
                self.loader = ui.linear_progress(show_value=False, size='40px', color='crimson')
                ui.label("Loading...").style("font-size: 50px; color: white; font-family: Lucida Console, Courier New, monospace")
                

    async def show(self):
        self.set_visibility(True)
        for i in range(100):
            self.loader.set_value(i/100.0)
            await asyncio.sleep(0.01)
    
    def hide(self):
        self.set_visibility(False)

def get_active():
    global sensors_active
    global ac_codes
    ac_codes = []
    sensors_active = ["Accel", "Strain", "Bevel"]
    for s in sensors_active:
        try:
            ac_codes.append(valid_codes_dict[s])
        except:
            print("Unsupported active sensor!")


def get_inactive():
    return ["Consectetur", "Adipiscing", "Elit"]

def was_resized(e):
    global width 
    width = e.args['width']
    global height
    height = e.args['height']
    print(width)
    print(height)

def parse_output_field():
    return [string.strip() for string in output_field.value.split(',')]

async def run_tests():
    global client
    filepaths = []
    in_string = '-f '
    test_string = ('-t ')
    load_dotenv()
    base_path = os.getenv("BASE_FILEPATH")
    for i, box in enumerate(boxes):
        if box.value == True:
            test_string += ac_codes[i]
            test_string += " "
    if parse_output_field()[0] != '':
        for entry in parse_output_field():
            in_string += entry
    else: # use names of tests if no filepaths given
        for code in test_string[2:].split():
            # configure these filepaths with your username and the location for your files!
            path = base_path + [k for k, v in valid_codes_dict.items() if v == code][0] + '.csv '
            filepaths.append(path)
            in_string += (base_path + [k for k, v in valid_codes_dict.items() if v == code][0] + '.csv ')
    in_string += test_string
    print(in_string)
    try:
        client.run_handler(in_string)
        print("Run handler ran successfully")
        return ', '.join(filepaths)
    except Exception as e:
        print(e)

def from_config():
    global client
    in_string = '-f '
    in_string += (json_field.value)
    try:
        client.json_handler(in_string)
    except Exception as e:
        print(e)

@ui.page('/')
async def index():
    global sensors_active
    global boxes
    global output_field
    global json_field
    global client
    global firstrun
    # make sure boxes are cleared
    boxes.clear()

    async def slow():
        task = asyncio.create_task(overlay.show())
        await asyncio.sleep(4)
        overlay.hide()

    with ui.row().classes('w-full h-20 flex justify-center items-center gap-4'):
        ui.label('Welcome to the VT Baja Testing Interface!').style("font-size: 50px; color: black; font-family: Lucida Console, Courier New, monospace; font-weight: bold").classes('w-full flex justify-center')

    with ui.grid(columns='1fr 2fr', rows=2).classes('w-full h-full gap-4'):
        with ui.column():
            ui.label("Active Sensors:").style("font-size: 40px; color: black; font-family: Lucida Console, Courier New, monospace")
            with ui.grid(columns='10fr 1fr'):
                get_active()
                for sensor in sensors_active:
                    ui.label("- " + sensor).style("font-size: 40px; color: green; font-family: Lucida Console, Courier New, monospace")
                    boxes.append(ui.checkbox())   
            ui.button('Run Tests', color = 'green').classes('flex justify-center w-xl').on('click', lambda: ui.navigate.to('/run'))
        with ui.column().classes('ml-30 gap-16 items justify-center'):
            ui.label("Run from configuration: ").style("font-size: 40px; color: black; font-family: Lucida Console, Courier New, monospace")
            json_field = ui.input(placeholder=r"Ex: C:\Users\<your username>\...\config.json").classes('flex justify-center w-2xl border p-5').style('border-width: 5px')
            ui.button('Run From Config', color = 'green').classes('flex justify-center w-2xl').on('click', lambda: from_config())
        with ui.column():
            ui.label("Inactive Sensors:").style("font-size: 40px; color: black; font-family: Lucida Console, Courier New, monospace")
            for sensor in get_inactive():
                ui.label("- " + sensor).style("font-size: 40px; color: red; font-family: Lucida Console, Courier New, monospace")
        with ui.column().classes('ml-30'):
            ui.label('Result Filepaths (Optional):').style("font-size: 30px; color: black; font-family: Lucida Console, Courier New, monospace")
            output_field = ui.input(label="Be sure to enter a path for every test you run to avoid errors!", placeholder=r"Ex. C:\Users\<your username>\...\accel.csv, C:\Users\<your username>\...\othertest.csv").classes('flex justify-center w-2xl border p-5').style('border-width: 5px')
            ui.label("System Information").style("font-size: 30px; color: black; font-family: Lucida Console, Courier New, monospace")
            ui.label("BajaCLI by vrusaeva v" + VERSION + " (alpha)").style("font-size: 20px; color: gray; font-family: Lucida Console, Courier New, monospace")
            ui.label("https://github.com/vrusaeva/BajaCLI").style("font-size: 20px; color: gray; font-family: Lucida Console, Courier New, monospace")
            ui.label("Please let me know of any issues!").style("font-size: 20px; color: gray; font-family: Lucida Console, Courier New, monospace")

    if (firstrun):
        overlay = Splash()
        app.on_connect(slow)
        firstrun = False

@ui.page('/run')
async def run_page():
    container = ui.column().classes('w-full h-full flex justify-center items-center gap-4')

    with container:
        ui.label("Running...").style("font-size: 40px; color: black; font-family: Lucida Console, Courier New, monospace")
        complete_label = ui.label("temp").style("font-size: 40px; color: black; font-family: Lucida Console, Courier New, monospace")
        back = ui.button('Back', color = 'green').classes('flex justify-center w-xl').on('click', lambda: ui.navigate.to('/'))
        complete_label.set_visibility(False)
        back.set_visibility(False)
        filepaths = await run_tests()
        complete_label.set_text(("Run complete. Saved results to " + filepaths))
        complete_label.set_visibility(True)
        back.set_visibility(True)

def shutdown():
    print("GUI closed, closing server...")

def run_gui():
    print("Starting GUI")
    app.on_shutdown(shutdown)
    try:
        ui.run(reload=False, port=8084)
        print("Started GUI")
    except Exception:
        traceback.print_exc()

# try:
#     ui.run()
# except Exception:
#     traceback.print_exc()
# app.on_shutdown(shutdown)