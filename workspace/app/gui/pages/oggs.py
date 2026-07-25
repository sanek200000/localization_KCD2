from pathlib import Path

from nicegui import run, ui
from nicegui.elements.button import Button
from nicegui.elements.label import Label
from nicegui.elements.spinner import Spinner

from app.api.oggs import get_oggs_count
from app.config import LOCALIZATION_PATH
from app.gui.layout import page_layout
from app.utils.parsers.counter import get_files_count_by_path

ogg_en_path = LOCALIZATION_PATH.joinpath("./en_voice_ogg")
wav_en_path = LOCALIZATION_PATH.joinpath("./en_voice_wav")
ogg_ru_path = LOCALIZATION_PATH.joinpath("./ru_voice_ogg")
wav_ru_path = LOCALIZATION_PATH.joinpath("./ru_voice_wav")


class OggsPage:
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

    @property
    def render_page(self):
        page_layout(self.content)


# class OggsPage_old:
#     async def handle_click(self, calc_button: Button, result_lable: Label):
#         calc_button.loading = True
#         result_lable.text = "Counting..."
#
#         try:
#             count = await asyncio.to_thread(
#                 get_files_count_by_path,
#                 path=LOCALIZATION_PATH.joinpath("./en_voice_ogg"),
#                 mask="*.ogg",
#             )
#             result_lable.text = f"Count files in ogg_en_path: {count}"
#         except Exception as ex:
#             result_lable.text = f"Error in counting: {ex}"
#         finally:
#             calc_button.loading = False
#
#     def content(self):
#         ui.label("OGG").classes("text-h4")
#
#         result_lable = ui.label("Count files in ogg_en_path: -")
#         calc_button = ui.button(
#             "get files count ogg_en_path",
#             on_click=lambda: self.handle_click(calc_button, result_lable),
#         )
#
#         ui.spinner(size="sm").bind_visibility_from(calc_button, "loading")
#
#     @property
#     def render_page(self):
#         page_layout(self.content)
