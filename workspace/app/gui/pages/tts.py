from nicegui import ui

from app.gui.layout import page_layaut


def tts_page():
    def content():
        ui.label("TTS").classes("text-h4")

    page_layaut(content)
