from pathlib import Path
from typing import Optional
from queue import Queue

from loguru import logger
from nicegui import run, ui
from nicegui.elements.button import Button
from nicegui.elements.label import Label
from nicegui.elements.log import Log
from nicegui.elements.spinner import Spinner

from app.api.oggs import get_oggs_count
from app.config import LOCALIZATION_PATH
from app.gui.layout import page_layout
from app.utils.ffmpeg_converter import convert_ogg_to_wav
from app.utils.parsers.counter import get_files_count_by_path

ogg_en_path = LOCALIZATION_PATH.joinpath("./en_voice_ogg")
wav_en_path = LOCALIZATION_PATH.joinpath("./en_voice_wav")
ogg_ru_path = LOCALIZATION_PATH.joinpath("./ru_voice_ogg")
wav_ru_path = LOCALIZATION_PATH.joinpath("./ru_voice_wav")


class OggsPage:
    def __init__(self) -> None:
        self.log: Optional[Log] = None
        self.queue: Queue[str] = Queue()
        self.sind_id: Optional[int] = None

    def start_log_capture(self):
        if self.sind_id is None:
            self.sind_id = logger.add(
                self.queue.put,
                format="{time:HH:mm:ss} | {level:<8} | {message}",
            )

    def stop_log_catrutre(self):
        if self.sind_id:
            logger.remove(self.sind_id)
            self.sind_id = None

    def update_log(self):
        while not self.queue.empty():
            self.log.push(self.queue.get())

    async def count_files(
        self, btn: Button, spnr: Spinner, label: Label, path: Path, mask: str
    ):
        btn.disable()
        spnr.visible = True
        label.set_text("Подсчет...")

        try:
            count = await run.io_bound(lambda: get_files_count_by_path(path, mask))
            label.set_text(f"{count}")
        finally:
            spnr.visible = False
            btn.enable()

    def add_ui_count(self, path: Path, mask: str):
        name = path.name

        with ui.row().classes("w-full items-stretch no-wrap"):
            with ui.column().classes("justify-center"):
                ui.label("Files count:").classes("w-full text-base")

            with ui.column().classes("flex-grow items-center"):
                with ui.row():
                    spinner = ui.spinner(size="lg")
                    spinner.visible = False

                    label = ui.label("_____").classes("text-base")

            with ui.column().classes("justify-center"):
                button = ui.button(
                    f"get files count {name}",
                    on_click=lambda: self.count_files(
                        btn=button,
                        spnr=spinner,
                        label=label,
                        path=path,
                        mask=mask,
                    ),
                )

    async def click_convert_oggs_to_wavs(self):
        self.log.clear()
        self.start_log_capture()

        try:
            await run.io_bound(convert_ogg_to_wav)
        finally:
            self.stop_log_catrutre()

    def get_count_oggs(self, label: Label):
        count = get_oggs_count(search=None)
        label.set_text(f"{count}")

    def content(self):
        ui.label("OGG").classes("text-h4")

        self.add_ui_count(ogg_en_path, "*.ogg")
        self.add_ui_count(wav_en_path, "*.wav")
        self.add_ui_count(ogg_ru_path, "*.ogg")
        self.add_ui_count(wav_ru_path, "*.wav")

        with ui.row().classes("w-full items-stretch no-wrap"):
            with ui.column().classes("justify-center"):
                ui.label("Oggs table count:").classes("w-full text-base")

            with ui.column().classes("flex-grow items-center"):
                label_oggs_count = ui.label("_____").classes("text-base")

            with ui.column().classes("justify-center"):
                ui.button(
                    "get count",
                    on_click=lambda: self.get_count_oggs(label_oggs_count),
                )

        ui.separator()
        with ui.row().classes("w-full items-stretch no-wrap"):
            with ui.column().classes("justify-center"):
                ui.button(
                    "convert oggs to wavs",
                    on_click=self.click_convert_oggs_to_wavs,
                )

            with ui.column().classes("w-full justify-center"):
                ui.label("Log").classes("text-h5")
                self.log = ui.log().classes("w-full").style("height: 350px")
                ui.timer(0.1, self.update_log)

    @property
    def render_page(self):
        page_layout(self.content)
