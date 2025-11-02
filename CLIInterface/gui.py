from nicegui import ui, app
import asyncio
import interface, server

VERSION = '0.6'
width = 0
height = 0

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
    return ["Accel", "Strain", "Bevel"]

def get_inactive():
    return ["Consectetur", "Adipiscing", "Elit"]

def was_resized(e):
    global width 
    width = e.args['width']
    global height
    height = e.args['height']
    print(width)
    print(height)


@ui.page('/')
async def index():
    async def slow():
        task = asyncio.create_task(overlay.show())
        await asyncio.sleep(4)
        overlay.hide()

    # Start the server and client
    # client = interface.CLIInterface()
    # sv = server.Network()
    # sv.create_and_listen()
    # sv.event_loop()

    with ui.row().classes('w-full h-20 flex justify-center items-center gap-4'):
        ui.label('Welcome to the VT Baja Testing Interface!').style("font-size: 50px; color: black; font-family: Lucida Console, Courier New, monospace; font-weight: bold").classes('w-full flex justify-center')

    with ui.grid(columns='1fr 2fr', rows=2).classes('w-full h-full gap-4'):
        with ui.column():
            ui.label("Active Sensors:").style("font-size: 40px; color: black; font-family: Lucida Console, Courier New, monospace")
            with ui.grid(columns='10fr 1fr'):
                for sensor in get_active():
                    ui.label("- " + sensor).style("font-size: 40px; color: green; font-family: Lucida Console, Courier New, monospace")
                    ui.checkbox()
            ui.button('Run Tests', color = 'green').classes('flex justify-center w-xl')
        with ui.column().classes('ml-30 gap-16 items justify-center'):
            ui.label("Run from configuration: ").style("font-size: 40px; color: black; font-family: Lucida Console, Courier New, monospace")
            ui.input(placeholder="Enter a filename...").classes('flex justify-center w-2xl border p-5').style('border-width: 5px')
            ui.button('Run From Config', color = 'green').classes('flex justify-center w-2xl')
        with ui.column():
            ui.label("Inactive Sensors:").style("font-size: 40px; color: black; font-family: Lucida Console, Courier New, monospace")
            for sensor in get_inactive():
                ui.label("- " + sensor).style("font-size: 40px; color: red; font-family: Lucida Console, Courier New, monospace")
        with ui.column().classes('ml-30'):
            ui.label('Result Filenames (Optional):').style("font-size: 30px; color: black; font-family: Lucida Console, Courier New, monospace")
            ui.input(placeholder="Defaults to sensor names. Separate with commas.").classes('flex justify-center w-2xl border p-5').style('border-width: 5px')
            ui.label("System Information").style("font-size: 30px; color: black; font-family: Lucida Console, Courier New, monospace")
            ui.label("BajaCLI by vrusaeva v" + VERSION + " (alpha)").style("font-size: 20px; color: gray; font-family: Lucida Console, Courier New, monospace")
            ui.label("https://github.com/vrusaeva/BajaCLI").style("font-size: 20px; color: gray; font-family: Lucida Console, Courier New, monospace")
            ui.label("Please let me know of any issues!").style("font-size: 20px; color: gray; font-family: Lucida Console, Courier New, monospace")

    overlay = Splash()
    app.on_connect(slow)



ui.run()