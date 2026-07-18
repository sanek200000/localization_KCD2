from nicegui import ui

from app.gui.layout import page_layaut


def subs_page():
    def content():
        ui.label("Subtitles").classes("text-h4")

    page_layaut(content)
