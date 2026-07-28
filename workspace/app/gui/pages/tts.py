from nicegui import ui

from app.gui.components.tts.area import TextareaTTSServer
from app.gui.components.tts.select import SelectModels, SelectServer
from app.gui.layout import page_layout
from app.utils.tts import check_ready_for_load_model


class TTSpage:
    def content(self):
        ui.label("TTS").classes("text-h4")

        area = TextareaTTSServer()
        SelectServer(area)

        if check_ready_for_load_model():
            SelectModels(area)

    @property
    def reder_page(self):
        page_layout(self.content)
