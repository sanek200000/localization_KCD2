from nicegui import ui, run

from app.api.tts import load_model


class SelectModels:
    def __init__(self, models: list):

        with ui.row().classes("justify-center items-center"):
            self.sl = ui.select(
                options=models,
                label="TTS models:",
                value=models[2],
            ).classes("text-base")

            self.btn = ui.button("load model", on_click=self.click_btn)
            self.spin = ui.spinner(size="lg")
            self.spin.visible = False

    async def click_btn(self):
        id = int(self.sl.value.split("|")[0])
        self.btn.disable()
        self.spin.visible = True

        try:
            await run.io_bound(lambda: load_model(id=id))
        finally:
            self.spin.visible = False
            self.btn.enable()

    @property
    def get_button(self):
        return self.btn
