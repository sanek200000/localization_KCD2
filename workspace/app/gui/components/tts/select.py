from nicegui import ui, run

from app.api.tts import change_tts_server, get_server_url, load_model
from app.gui.components.tts.area import TextareaTTSServer
from app.gui.services.tts import GetTTSModels


class SelectModels:
    def __init__(self, area: TextareaTTSServer):
        self._area = area
        models = GetTTSModels.get_list()

        with ui.row().classes("w-full justify-center items-center no-wrap"):
            self.sl = ui.select(
                options=models,
                label="TTS models:",
                value=models[2],
            ).classes("w-full text-base")

            with ui.column().classes("w-65 items-center"):
                self.btn = ui.button("load model", on_click=self.click_btn).classes(
                    "ml-auto"
                )
                self.spin = ui.spinner(size="lg")
                self.spin.visible = False

    async def click_btn(self):
        id = int(self.sl.value.split("|")[0])
        self.btn.visible = False
        self.spin.visible = True

        try:
            await run.io_bound(lambda: load_model(id=id))
            await self._area.refresh()
        finally:
            self.spin.visible = False
            self.btn.visible = True

    @property
    def button(self):
        return self.btn


class SelectServer:
    def __init__(self, area: TextareaTTSServer) -> None:
        self._area = area
        url = get_server_url()

        with ui.row().classes("w-full justify-center items-center no-wrap"):
            ui.label("URL: ")
            self.inp = ui.input(value=url).classes("w-full text-base")

            with ui.column().classes("w-70 items-center"):
                self.btn = ui.button(
                    "change connection", on_click=self.click_btn
                ).classes("ml-auto")
                self.spin = ui.spinner(size="lg")
                self.spin.visible = False

    async def click_btn(self):
        self.btn.visible = False
        self.spin.visible = True

        try:
            await run.io_bound(lambda: change_tts_server(url=self.inp.value))
            await self._area.refresh()
        finally:
            self.spin.visible = False
            self.btn.visible = True
