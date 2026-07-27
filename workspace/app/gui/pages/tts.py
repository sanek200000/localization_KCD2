from nicegui import ui

from app.gui.components.tts.select import SelectModels
from app.gui.layout import page_layout
from app.gui.services.tts import GetTTSModels


class TTSpage:
    def __init__(self) -> None:
        self.models = GetTTSModels.get_list()

    def content(self):
        ui.label("TTS").classes("text-h4")

        if self.models:
            btn_load_models = SelectModels(self.models)

    @property
    def reder_page(self):
        page_layout(self.content)
