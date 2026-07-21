from nicegui import ui

from app.gui.layout import page_layout


def home_page():
    def content():
        ui.label("Dashboard").classes("text-h4")
        ui.separator()
        ui.label("Wellcome to KCD2 localization")

    page_layout(content)
