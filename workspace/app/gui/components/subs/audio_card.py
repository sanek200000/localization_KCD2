from pathlib import Path

from nicegui import ui
from app.repositories.mappers.mappers import OggDTO


class AudioCard:
    def __init__(self, ogg: OggDTO) -> None:
        with ui.card().classes("w-full"):
            ui.label(ogg.name).classes("text-h6")
            ui.separator()

            ui.label("English")
            if ogg.wav_en_path:
                ui.audio(Path(ogg.wav_en_path)).classes("w-full")
                # ui.button('Delete en wav')
            else:
                ui.label("No WAV")
            ui.separator()

            ui.label("Russian")
            if ogg.wav_ru_path:
                ui.audio(Path(ogg.wav_ru_path)).classes("w-full")
                ui.button("Delete ru wav")
            else:
                ui.label("No WAV")
