from loguru import logger
from nicegui import ui
from pathlib import Path

from app.api.subs import delete_sub, patch_sub
from app.api.tts import convert_audio_with_remote_session
from app.gui.components.audio_playlist import AudioPlaylist
from app.gui.components.subs.editor import EditorBody
from app.gui.services.subs import GuiSubsService
from app.gui.layout import page_layout
from app.schemas.oggs import OggDTO
from app.schemas.subs import SubPatchDTO
from app.gui.state.subs import navigation_state as ns


class SubsEditorPage:
    def __init__(self, sub_id: int) -> None:
        self.sub = GuiSubsService.get(sub_id)

        self.ids = ns.ids
        if self.sub.id in self.ids:
            self.current_index = self.ids.index(self.sub.id)
        else:
            ns.restore(self.sub.id)
            self.ids = ns.ids
            self.current_index = self.ids.index(self.sub.id)

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

    def content(self):
        with ui.row().classes("w-full items-stretch no-wrap"):
            with ui.column().classes("justify-center"):
                prev_button = ui.button("<<", on_click=self.open_prev).classes("h-full")
                prev_button.enabled = self.current_index > 0 or ns.page > 0

            with ui.column().classes("flex-grow"):
                eb = EditorBody(
                    sub=self.sub,
                    ids=self.ids,
                    current_index=self.current_index,
                )

            with ui.column().classes("justify-center"):
                next_button = ui.button(">>", on_click=self.open_next).classes("h-full")
                next_button.enabled = (
                    self.current_index < len(self.ids) - 1 or ns.page < ns.pages - 1
                )

            ui.timer(0.1, eb.playlist.start, once=True)

    @property
    def render_page(self):
        page_layout(self.content)
