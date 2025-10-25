from nicegui import ui, app
import asyncio

class Splash(ui.element):
    def __init__(self):
        super().__init__(tag='div')
        self.style('position: fixed; display: block; width: 100%; height: 100%;'
                   'top: 0; left: 0; right: 0; bottom: 0; z-index: 2; cursor: pointer;'
                   'background-color:' + f'rgba{(134, 31, 65, 0.5)};')        
        with self:
            with ui.element('div').classes("h-screen flex items-center justify-center"):
                ui.image('https://i.postimg.cc/jqWLZTXZ/Screenshot-2025-10-25-151405.png')
                self.loader = ui.linear_progress(show_value=False, size='40px', color='crimson')
                ui.label("Loading...").style("font-size: 50px; color: white; font-family: Lucida Console, Courier New, monospace")
                

    async def show(self):
        self.set_visibility(True)
        for i in range(1000):
            self.loader.set_value(i/1000.0)
            await asyncio.sleep(0.001)
            print(self.loader.value)
    
    def hide(self):
        self.set_visibility(False)

@ui.page('/')
async def index():
    async def slow():
        task = asyncio.create_task(overlay.show())
        await asyncio.sleep(4)
        overlay.hide()
    
    ui.label('wip')
    overlay = Splash()
    app.on_connect(slow)

ui.run()