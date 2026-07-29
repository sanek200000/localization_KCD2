from nicegui import ui, run

from app.api.tts import get_server_url, load_model
from app.config import RS
from app.gui.components.tts.area import TextareaTTSServer
from app.gui.services.tts import GetTTSModels
from app.utils.tts import check_ready_for_load_model


class SelectModels:
    def __init__(self, reload_components):
        self.reload_components = reload_components

        ui.timer(0.1, self.refresh, once=True)

    async def refresh(self):
        models = list()
        check = await run.io_bound(check_ready_for_load_model)

        if check:
            models = GetTTSModels.get_list()

        with ui.row().classes(
            "w-full justify-center items-center no-wrap"
        ) as self.root:
            self.sl = ui.select(
                options=models,
                label="TTS models:",
                value=models[0] if models else None,
            ).classes("w-full text-base")

            with ui.column().classes("w-65 items-center"):
                self.btn = ui.button("load model", on_click=self.click_btn).classes(
                    "ml-auto"
                )
                self.spin = ui.spinner(size="lg")
                self.spin.visible = False

        self.root.set_visibility(check)

    async def click_btn(self):
        id = int(self.sl.value.split("|")[0])
        self.btn.visible = False
        self.spin.visible = True

        try:
            await run.io_bound(lambda: load_model(id=id))
            await self.reload_components()
            # await self._area.refresh()
        finally:
            self.spin.visible = False
            self.btn.visible = True

    @property
    def button(self):
        return self.btn


class SelectServer:
    def __init__(self, reload_components) -> None:
        self.reload_components = reload_components
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
            RS.tts_server_url = self.inp.value
            await self.reload_components()
        finally:
            self.spin.visible = False
            self.btn.visible = True
