from nicegui import ui
from pathlib import Path

from app.api.subs import delete_sub, patch_sub
from app.gui.services.subs import GuiSubsService
from app.gui.layout import page_layout
from app.schemas.oggs import OggDTO
from app.schemas.subs import SubPatchDTO
from app.gui.state.subs import navigation_state as ns


def save():
    patch_sub(
        sub_id=sub.id,
        data=SubPatchDTO(ru_sub=ru_sub.value, ru_accent=ru_accent.value),
    )
    ui.notify("Изменения сохранены", type="positive")


def delete():
    delete_sub(sub_id=sub.id)
    ui.notify("Запись удалена", type="positive")
    ui.navigate.to("/subs")


def delete_wav(path: str):
    file = Path(path)
    file.unlink(missing_ok=True)
    ui.notify("File deleted", type="positive")
    ui.navigate.to(f"/subs/{sub.id}")


def create_voice_block(ogg: OggDTO):
    with ui.card().classes("w-full"):
        ui.label(ogg.name).classes("text-h6")
        ui.separator()

        if Path(ogg.wav_en_path).exists():
            ui.label("English")
            ui.audio(ogg.wav_en_path).classes("w-full")

        if Path(ogg.wav_ru_path).exists():
            ui.label("Russian")
            ui.audio(ogg.wav_ru_path).classes("w-full")
            ui.button("Delete WAV", on_click=lambda p=ogg.wav_ru_path: delete_wav(p))


def subs_editor_page(sub_id: int):
    sub = GuiSubsService.get(sub_id)
    ids = ns.ids
    currnt_index = ids.index(sub.id)

    def open_prev():
        if currnt_index > 0:
            ui.navigate.to(f"/subs/{ids[currnt_index - 1]}")
            return

        if ns.page == 0:
            return

        ns.page -= 1
        ns.reload()

        ui.navigate.to(f"/subs/{ns.ids[-1]}")

    def open_next():
        if currnt_index < len(ids) - 1:
            ui.navigate.to(f"/subs/{ids[currnt_index + 1]}")
            return

        if ns.page >= ns.pages - 1:
            return

        ns.page += 1
        ns.reload()

        ui.navigate.to(f"/subs/{ns.ids[0]}")

    def content():
        with ui.dialog() as dialog, ui.card():
            ui.label("Delete subtitle?")
            with ui.row():
                ui.button("NO", on_click=dialog.close)
                ui.button("YES", on_click=lambda: (dialog.close(), delete())).props(
                    "color=negative"
                )

        with ui.row().classes("w-full items-center justify-between"):
            prev_button = ui.button("← Предыдущая", on_click=open_prev)
            prev_button.enabled = currnt_index > 0 or ns.page > 0
            ui.label(f"ID {sub.id}").classes("text-h5")
            next_button = ui.button("Следующая →", on_click=open_next)
            next_button.enabled = currnt_index < len(ids) - 1 or ns.page < ns.pages - 1
            ui.separator()

            ui.label("KEY:").classes("text-h6")
            ui.label(sub.key).style("white-space: pre-wrap; font-size:16px")
            ui.separator()

            ui.label("English:").classes("text-h6")
            ui.label(sub.en_sub).style("white-space: pre-wrap; font-size:16px")
            ui.separator()

            ui.label("Russian:").classes("text-h6")
            ru_sub = (
                ui.textarea(value=sub.ru_sub)
                .props("rows=2")
                .classes("w-full text-base")
            )
            ru_accent = (
                ui.textarea(value=sub.ru_accent)
                .props("rows=2")
                .classes("w-full text-base")
            )
            ui.separator()

            ui.label("Voices").classes("text-h5")
            for ogg in sub.oggs:
                create_voice_block(ogg)

            ui.separator()

            with ui.row():
                ui.button("💾 Save", on_click=save)
                ui.button("🗑 Delete subtitle", on_click=dialog.open).props(
                    "color=negative"
                )

    page_layout(content)
