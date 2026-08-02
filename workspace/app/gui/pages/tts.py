from nicegui import ui

from app.api.tts import streaming_conversion
from app.gui.components.tts.area import TextareaTTSServer
from app.gui.components.tts.process_runner import ProcessRunner
from app.gui.components.tts.select import SelectModels, SelectServer
from app.gui.layout import page_layout
from app.utils.tts import check_ready_for_load_model, check_ready_tts_server


class TTSpage:
    async def reload(self):
        await self.area.refresh()
        await self.sm.refresh()
        await self.pr.refresh()

    def content(self):
        ui.label("TTS").classes("text-h4")

        self.area = TextareaTTSServer()
        SelectServer(self.reload)

        self.sm = SelectModels(self.reload)

        self.pr = ProcessRunner("app.cli.streaming_conversion")

        ui.timer(0.1, self.reload, once=True)

    @property
    def reder_page(self):
        page_layout(self.content)
