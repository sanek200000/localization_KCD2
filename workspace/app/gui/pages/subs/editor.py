from nicegui import ui
from pathlib import Path

from app.gui.services.subs import GuiSubsService
from app.gui.layout import page_layout
from app.schemas.oggs import OggDTO


def create_voice_block(ogg: OggDTO):
    with ui.card().classes("w-full"):
        ui.label(ogg.name).classes("text-h6")
        ui.separator()

        if Path(ogg.wav_en_path).exists():
            ui.label("English")
            ui.audio(ogg.wav_en_path).classes("w-full")

        if Path(ogg.wav_ru_path).exists():
            ui.label("Russian")
            ui.audio(ogg.wav_ru_path).classes("w-full")
            ui.button("Delete WAV")


def subs_editor_page(sub_id: int):
    sub = GuiSubsService.get(sub_id)

    def content():
        with ui.row().classes("items-center"):
            ui.button("← Назад", on_click=lambda: ui.navigate.to("/subs"))
            ui.label(f"ID {sub.id}").classes("text-h5")
            ui.separator()

            ui.label("KEY")
            ui.input(value=sub.key).props("readonly").classes("w-full")

            ui.label("English")
            ui.textarea(value=sub.en_sub).props("readonly").classes("w-full")

            ui.label("Russian")
            ru_sub = ui.textarea(value=sub.ru_sub).classes("w-full")
            ru_accent = ui.textarea(value=sub.ru_accent).classes("w-full")
            ui.separator()

            ui.label("Voices").classes("text-h5")
            for ogg in sub.oggs:
                create_voice_block(ogg)

            ui.separator()

            with ui.row():
                ui.button("")
                ui.button("").props("color=negative")

    page_layout(content)
