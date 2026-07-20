from nicegui import ui

from app.gui.components.pager import Pager
from app.gui.components.subs.grid_mapper import to_grid_row
from app.gui.components.subs.table import SubsTable
from app.gui.components.subs.toolbar import SubsToolbar
from app.gui.layout import page_layaut
from app.gui.services.subs import GuiSubsService


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
        # rows = list()
        #
        # for sub in service.get_page(
        #     offset=offset,
        #     limit=limit,
        #     search=current_search,
        # ):
        #     # en_audio = any(ogg.wav_en_path for ogg in sub.oggs)
        #     # ru_audio = any(ogg.wav_ru_path for ogg in sub.oggs)
        #
        #     rows.append(
        #         {
        #             "id": sub.id,
        #             "key": sub.key,
        #             "en_sub": sub.en_sub,
        #             "ru_sub": sub.ru_sub,
        #             "accent": sub.ru_accent,
        #             # "en_audio": "✔" if en_audio else "",
        #             # "ru_audio": "✔" if ru_audio else "",
        #             "audio_count": len(sub.oggs),
        #         }
        #     )

        rows = [
            to_grid_row(sub)
            for sub in service.get_page(
                offset=offset,
                limit=limit,
                search=current_search,
            )
        ]
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

    page_layaut(content)
