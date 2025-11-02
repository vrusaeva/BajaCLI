from nicegui import ui, app
import asyncio
import interface

# GUI to interact with Baja CLI interface.
# 
# Author: vrusaeva
# Version: v0.7 (11/02/2025)

VERSION = '0.7'
width = 0
height = 0

sensors_active = []
ac_codes = []
valid_codes_dict = {"Accel": 'a', "Strain": 's', "Bevel": 'b'}

boxes = []
json_field = None
output_field = None
filepaths = [] # for output

client = interface.CLIInterface()

class Splash(ui.element):
    def __init__(self):
        super().__init__(tag='div')
        self.style('position: fixed; display: block; width: 100%; height: 100%;'
                   'top: 0; left: 0; right: 0; bottom: 0; z-index: 2; cursor: pointer;'
                   'background-color:' + f'rgba{(134, 31, 65, 0.75)};')        
        with self:
            with ui.element('div').classes("h-screen flex items-center justify-center"):
                ui.image('https://i.postimg.cc/jqWLZTXZ/Screenshot-2025-10-25-151405.png').classes('h-auto max-w-4xl rounded-lg flex justify-center')
                self.loader = ui.linear_progress(show_value=False, size='40px', color='crimson')
                ui.label("Loading...").style("font-size: 50px; color: white; font-family: Lucida Console, Courier New, monospace")
                

    async def show(self):
        self.set_visibility(True)
        for i in range(1000):
            self.loader.set_value(i/1000.0)
            await asyncio.sleep(0.001)
    
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

def run_tests():
    global client
    global filepaths
    in_string = '-f '
    test_string = ('-t ')
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
            path = r'C:\Users\vrusa\OneDrive\Documents\BajaCLI\\' + [k for k, v in valid_codes_dict.items() if v == code][0] + '.csv '
            filepaths.append(path)
            in_string += (r'C:\Users\vrusa\OneDrive\Documents\BajaCLI\\' + [k for k, v in valid_codes_dict.items() if v == code][0] + '.csv ')
    in_string += test_string
    print(in_string)
    try:
        client.run_handler(in_string)
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

    async def slow():
        task = asyncio.create_task(overlay.show())
        await asyncio.sleep(4)
        overlay.hide()

    # Start the server and client
    # sv = server.Network()
    # sv.create_and_listen()
    # sv.event_loop()

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
            ui.button('Run Tests', color = 'green').classes('flex justify-center w-xl').on('click', lambda: run_tests())
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

    overlay = Splash()
    app.on_connect(slow)



ui.run()