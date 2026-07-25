from typing import Optional

from nicegui import ui

from app.gui.components.pager import Pager
from app.gui.components.subs.grid_mapper import to_grid_row
from app.gui.components.subs.table import SubsTable
from app.gui.components.subs.toolbar import SubsToolbar
from app.gui.layout import page_layout
from app.gui.services.subs import GuiSubsService
from app.gui.state.subs import navigation_state as ns


class SubsTablePage:
    def __init__(self) -> None:
        self.service = GuiSubsService
        self.table: Optional[SubsTable] = None
        self.pager: Optional[Pager] = None
        self.current_search = ""

    def open_sub(self, sub_id: int):
        try:
            self.service.get(sub_id)
        except Exception:
            ui.notify(f"Subtitle {sub_id} not found", type="negative")
            return

        ui.navigate.to(f"/subs/{sub_id}")

    def search(self, text: str):
        self.current_search = text
        self.pager.page = 0
        self.pager.set_total(self.service.count(text))
        self.pager.emit()

    def load(self, offset: int, limit: int):
        ns.page = offset // limit
        ns.page_size = limit
        ns.search = self.current_search
        ns.reload()

        rows = [to_grid_row(sub) for sub in ns.rows]

        self.table.set_rows(rows)

    def content(self):
        with ui.column().classes("w-full items-center"):
            SubsToolbar(on_search=self.load, on_open_id=self.open_sub)

            ui.separator()
            self.pager = Pager(page_size=20, on_change=self.load)
            self.table = SubsTable(on_open=self.open_sub)
            self.pager.set_total(self.service.count())
            self.pager.emit()

    @property
    def render_page(self):
        page_layout(self.content)
