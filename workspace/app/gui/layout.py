from typing import Callable

from nicegui import ui

from app.gui.components.header import create_header
from app.gui.components.sidebar import create_sidebar


def page_layaut(content: Callable[[], None]) -> None:
    create_header()

    with ui.row().classes("w-full no-wrap"):
        with ui.column().classes("w-64 bg-grey-2 h-screen"):
            create_sidebar()

        with ui.column().classes("flex-grow p-4"):
            content()
