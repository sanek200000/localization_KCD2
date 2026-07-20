from nicegui import ui

from app.gui.components.subs.table import SubsTable
from app.gui.components.subs.toolbar import SubsToolbar
from app.gui.layout import page_layaut
from app.gui.services.subs import GuiSubsService


def subs_table_page():
    table = None

    def open_sub(sub_id: int):
        ui.navigate.to(f"/subs/{sub_id}")

    def load(search: str = ""):
        rows = list()

        for sub in GuiSubsService.get_page(offset=0, limit=100, search=search):
            en_audio = any(ogg.wav_en_path for ogg in sub.oggs)
            ru_audio = any(ogg.wav_ru_path for ogg in sub.oggs)

            rows.append(
                {
                    "id": sub.id,
                    "key": sub.key,
                    "en_sub": sub.en_sub,
                    "ru_sub": sub.ru_sub,
                    "accent": sub.ru_accent,
                    "en_audio": "✔" if en_audio else "",
                    "ru_audio": "✔" if ru_audio else "",
                }
            )

        table.set_rows(rows)

    def content():
        nonlocal table

        SubsToolbar(on_search=load, on_open_id=open_sub)

        ui.separator()
        table = SubsTable(on_open=open_sub)
        load()

    page_layaut(content)
