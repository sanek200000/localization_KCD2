from nicegui import ui

from app.api.tts import streaming_conversion
from app.gui.components.tts.area import TextareaTTSServer
from app.gui.components.tts.process_runner import ProcessRunner
from app.gui.components.tts.select import SelectModels, SelectServer
from app.gui.layout import page_layout
from app.utils.tts import check_ready_for_load_model, check_ready_tts_server


class TTSpage:
    def content(self):
        ui.label("TTS").classes("text-h4")

        area = TextareaTTSServer()
        SelectServer(area)

        if check_ready_for_load_model():
            SelectModels(area)

        if check_ready_tts_server():
            # ui.button("start", on_click=lambda: streaming_conversion(limit=4))
            ProcessRunner("app.cli.streaming_conversion", "--limit", "10")

    @property
    def reder_page(self):
        page_layout(self.content)
