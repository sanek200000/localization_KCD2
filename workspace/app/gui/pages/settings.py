from nicegui import ui

from app.gui.layout import page_layout


def settings_page():
    def content():
        ui.label("Settings").classes("text-h4")

    page_layout(content)
