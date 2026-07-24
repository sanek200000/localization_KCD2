from loguru import logger
from nicegui import ui
from pathlib import Path

from app.api.subs import delete_sub, patch_sub
from app.api.tts import convert_audio_with_remote_session
from app.gui.components.audio_playlist import AudioPlaylist
from app.gui.services.subs import GuiSubsService
from app.gui.layout import page_layout
from app.schemas.oggs import OggDTO
from app.schemas.subs import SubPatchDTO
from app.gui.state.subs import navigation_state as ns


class SubsEditorPage:
    def __init__(self, sub_id: int) -> None:
        self.sub = GuiSubsService.get(sub_id)
        self.playlist = AudioPlaylist()

        self.ids = ns.ids
        if self.sub.id in self.ids:
            self.current_index = self.ids.index(self.sub.id)
        else:
            ns.restore(self.sub.id)
            self.ids = ns.ids
            self.current_index = self.ids.index(self.sub.id)

    def save(self):
        patch_sub(
            sub_id=self.sub.id,
            data=SubPatchDTO(
                ru_sub=self.ru_sub.value,
                ru_accent=self.ru_accent.value,
            ),
        )
        ui.notify("Изменения сохранены", type="positive")

    def delete(self):
        delete_sub(sub_id=self.sub.id)
        ui.notify("Запись удалена", type="positive")
        self.ids.pop(self.sub.id)
        ui.navigate.to(f"/subs/{self.ids[self.current_index]}")

    def delete_wav(self, path: str):
        file = Path(path)
        file.unlink(missing_ok=True)
        ui.notify("File deleted", type="positive")
        ui.navigate.to(f"/subs/{self.sub.id}")

    def voice_render(self, path):
        self.delete_wav(path)
        convert_audio_with_remote_session(sub=self.sub)
        ui.notify("File rendered", type="positive")

    def open_prev(self):
        if self.current_index is None:
            return

        if self.current_index > 0:
            ui.navigate.to(f"/subs/{self.ids[self.current_index - 1]}")
            return

        if ns.page == 0:
            return

        ns.page -= 1
        ns.reload()

        ui.navigate.to(f"/subs/{ns.ids[-1]}")

    def open_next(self):
        if self.current_index is None:
            return

        if self.current_index < len(self.ids) - 1:
            ui.navigate.to(f"/subs/{self.ids[self.current_index + 1]}")
            return

        if ns.page >= ns.pages - 1:
            return

        ns.page += 1
        ns.reload()

        ui.navigate.to(f"/subs/{ns.ids[0]}")

    def create_voice_block(self, ogg: OggDTO):
        with ui.card().classes("w-full"):
            ui.label(ogg.name).classes("text-h6")
            ui.separator()

            ui.label("English")
            if Path(ogg.wav_en_path).exists():
                en_voice = ui.audio(ogg.wav_en_path).classes("w-full")
                self.playlist.add(en_voice)

            ui.label("Russian")
            with ui.row().classes("w-full items-center"):
                if Path(ogg.wav_ru_path).exists():
                    ru_voice = ui.audio(ogg.wav_ru_path).classes("flex-grow")
                    self.playlist.add(ru_voice)

                    ui.button(
                        "Delete WAV",
                        on_click=lambda p=ogg.wav_ru_path: self.delete_wav(p),
                    ).props("color=negative")

                ui.button(
                    "Render",
                    on_click=lambda p=ogg.wav_ru_path: self.voice_render(p),
                ).props("color=green")

    def body(self):
        with ui.dialog() as dialog, ui.card():
            ui.label("Delete subtitle?")
            with ui.row():
                ui.button("NO", on_click=dialog.close)
                ui.button(
                    "YES",
                    on_click=lambda: (
                        dialog.close(),
                        self.delete(),
                    ),
                ).props("color=negative")

        with ui.row().classes("w-full items-center justify-between"):
            ui.label(f"ID {self.sub.id}").classes("text-h5")
            ui.separator()

            with ui.row().classes("items-center no-wrap"):
                ui.label("key:").classes("text-h6").style("min-width: 100px")
                ui.label(self.sub.key).style("white-space: pre-wrap; font-size:16px")
            ui.separator()

            with ui.row().classes("items-center no-wrap"):
                ui.label("English:").classes("text-h6").style("min-width: 100px")
                ui.label(self.sub.en_sub).style("white-space: pre-wrap; font-size:16px")
            ui.separator()

            with ui.row().classes("w-full items-start"):
                ui.label("Russian:").classes("text-h6").style("min-width: 100px")

                with ui.column().classes("flex-grow gap-2"):
                    self.ru_sub = (
                        ui.textarea(value=self.sub.ru_sub)
                        .props("rows=2")
                        .classes("w-full text-base")
                    )
                    self.ru_accent = (
                        ui.textarea(value=self.sub.ru_accent)
                        .props("rows=2")
                        .classes("w-full text-base")
                    )
            ui.separator()

            ui.label("Voices").classes("text-h5")
            for ogg in self.sub.oggs:
                self.create_voice_block(ogg)

            ui.separator()

            with ui.row().classes("items-center"):
                ui.button("💾 Save", on_click=self.save)
                ui.button("🗑 Delete subtitle", on_click=dialog.open).props(
                    "color=negative"
                )

    def content(self):
        with ui.row().classes("w-full items-stretch no-wrap"):
            with ui.column().classes("justify-center"):
                prev_button = ui.button("<<", on_click=self.open_prev).classes("h-full")
                prev_button.enabled = self.current_index > 0 or ns.page > 0

            with ui.column().classes("flex-grow"):
                self.body()

            with ui.column().classes("justify-center"):
                next_button = ui.button(">>", on_click=self.open_next).classes("h-full")
                next_button.enabled = (
                    self.current_index < len(self.ids) - 1 or ns.page < ns.pages - 1
                )

            ui.timer(0.1, self.playlist.start, once=True)

    @property
    def render_page(self):
        page_layout(self.content)
