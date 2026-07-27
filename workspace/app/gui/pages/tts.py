from nicegui import ui

from app.gui.components.tts.area import TextareaTTSServer
from app.gui.components.tts.select import SelectModels
from app.gui.layout import page_layout
from app.gui.services.tts import GetTTSModels


class TTSpage:
    def __init__(self) -> None:
        self.models = GetTTSModels.get_list()

    def content(self):
        ui.label("TTS").classes("text-h4")

        area = TextareaTTSServer()
        area.area

        if self.models:
            btn_load_models = SelectModels(self.models).get_button
            area.refresh()

    @property
    def reder_page(self):
        page_layout(self.content)
