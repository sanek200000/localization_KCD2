from nicegui import ui

from app.gui.layout import page_layout


def oggs_page():
    def content():
        ui.label("OGG").classes("text-h4")

    page_layout(content)
