from collections.abc import Callable

from nicegui import ui


class SubsToolbar:
    def __init__(
        self,
        on_search: Callable[[str], None],
        on_open_id: Callable[[int], None],
    ) -> None:
        self.search = ui.input(label="Search by key")
        self.id_input = ui.number(label="ID", value=0, precision=0)

        with ui.row():
            ui.button("Search", on_click=lambda: on_search(self.search.value.strip()))
            ui.button("Open ID", on_click=lambda: on_open_id(int(self.id_input.value)))
