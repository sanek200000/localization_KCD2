from nicegui import ui

from app.gui.components.pager import Pager
from app.gui.components.subs.grid_mapper import to_grid_row
from app.gui.components.subs.table import SubsTable
from app.gui.components.subs.toolbar import SubsToolbar
from app.gui.layout import page_layout
from app.gui.services.subs import GuiSubsService
from app.gui.state.subs import navigation_state as ns


def subs_table_page():
    service = GuiSubsService
    table = None
    pager = None
    current_search = ""

    def open_sub(sub_id: int):
        ui.navigate.to(f"/subs/{sub_id}")

    def search(text: str):
        nonlocal current_search

        current_search = text
        pager.page = 0
        pager.set_total(service.count(text))
        pager.emit()

    def load(offset: int, limit: int):
        ns.page = offset // limit
        ns.page_size = limit
        ns.search = current_search
        ns.reload()

        rows = [to_grid_row(sub) for sub in ns.rows]

        table.set_rows(rows)

    def content():
        nonlocal table
        nonlocal pager

        with ui.column().classes("w-full h-full"):
            SubsToolbar(on_search=load, on_open_id=open_sub)

            ui.separator()
            table = SubsTable(on_open=open_sub)
            pager = Pager(page_size=20, on_change=load)
            pager.set_total(service.count())
            pager.emit()

    page_layout(content)
