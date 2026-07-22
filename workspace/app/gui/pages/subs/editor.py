from nicegui import ui
from pathlib import Path

from app.api.subs import delete_sub, patch_sub
from app.gui.services.subs import GuiSubsService
from app.gui.layout import page_layout
from app.schemas.oggs import OggDTO
from app.schemas.subs import SubPatchDTO
from app.gui.state.subs import navigation_state as ns


def subs_editor_page(sub_id: int):
    sub = GuiSubsService.get(sub_id)
    ids = ns.ids
    current_index = ids.index(sub.id)

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

    def open_prev():
        if current_index > 0:
            ui.navigate.to(f"/subs/{ids[current_index - 1]}")
            return

        if ns.page == 0:
            return

        ns.page -= 1
        ns.reload()

        ui.navigate.to(f"/subs/{ns.ids[-1]}")

    def create_voice_block(ogg: OggDTO):
        with ui.card().classes("w-full"):
            ui.label(ogg.name).classes("text-h6")
            ui.separator()

            if Path(ogg.wav_en_path).exists():
                ui.label("English")
                ui.audio(ogg.wav_en_path).classes("w-full").props("autoplay")

            if Path(ogg.wav_ru_path).exists():
                ui.label("Russian")
                with ui.row().classes("w-full items-center"):
                    ui.audio(ogg.wav_ru_path).classes("flex-grow").props("autoplay")
                    ui.button(
                        "Delete WAV", on_click=lambda p=ogg.wav_ru_path: delete_wav(p)
                    ).props("color=negative")

    def open_next():
        if current_index < len(ids) - 1:
            ui.navigate.to(f"/subs/{ids[current_index + 1]}")
            return

        if ns.page >= ns.pages - 1:
            return

        ns.page += 1
        ns.reload()

        ui.navigate.to(f"/subs/{ns.ids[0]}")

    def body():
        with ui.dialog() as dialog, ui.card():
            ui.label("Delete subtitle?")
            with ui.row():
                ui.button("NO", on_click=dialog.close)
                ui.button("YES", on_click=lambda: (dialog.close(), delete())).props(
                    "color=negative"
                )

        with ui.row().classes("w-full items-center justify-between"):
            ui.label(f"ID {sub.id}").classes("text-h5")
            ui.separator()

            with ui.row().classes("items-center no-wrap"):
                ui.label("key:").classes("text-h6")
                ui.label(sub.key).style("white-space: pre-wrap; font-size:16px")
            ui.separator()

            with ui.row().classes("items-center no-wrap"):
                ui.label("English:").classes("text-h6")
                ui.label(sub.en_sub).style("white-space: pre-wrap; font-size:16px")
            ui.separator()

            with ui.row().classes("w-full no-wrap"):
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

            with ui.row().classes("items-center"):
                ui.button("💾 Save", on_click=save)
                ui.button("🗑 Delete subtitle", on_click=dialog.open).props(
                    "color=negative"
                )

    def content():
        with ui.row().classes("w-full h-full no-wrap"):
            prev_button = ui.button("<<", on_click=open_prev).classes("h-full")
            prev_button.enabled = current_index > 0 or ns.page > 0

            body()

            next_button = ui.button(">>", on_click=open_next)
            next_button.enabled = current_index < len(ids) - 1 or ns.page < ns.pages - 1

    page_layout(content)
