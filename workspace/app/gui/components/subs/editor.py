from pathlib import Path

from loguru import logger
from nicegui import run, ui

from app.api.subs import delete_sub, patch_sub
from app.api.tts import convert_audio_with_remote_session
from app.gui.components.audio_playlist import AudioPlaylist
from app.schemas.oggs import OggDTO
from app.schemas.subs import SubDTO, SubPatchDTO


class EditorBody:
    def __init__(self, sub: SubDTO, ids: list[int], current_index: int) -> None:
        self._sub = sub
        self._ids = ids
        self._current_index = current_index
        self._playlist = AudioPlaylist()

        with ui.row().classes("w-full items-center justify-between"):
            ui.label(f"ID {self._sub.id}").classes("text-h5")
            ui.separator()

            with ui.row().classes("items-center no-wrap"):
                ui.label("key:").classes("text-h6").style("min-width: 100px")
                ui.label(self._sub.key).style("white-space: pre-wrap; font-size:16px")
            ui.separator()

            with ui.row().classes("items-center no-wrap"):
                ui.label("English:").classes("text-h6").style("min-width: 100px")
                ui.label(self._sub.en_sub).style(
                    "white-space: pre-wrap; font-size:16px"
                )
            ui.separator()

            with ui.row().classes("w-full items-start"):
                ui.label("Russian:").classes("text-h6").style("min-width: 100px")

                with ui.column().classes("flex-grow gap-2"):
                    self._ru_sub = (
                        ui.textarea(value=self._sub.ru_sub)
                        .props("rows=2")
                        .classes("w-full text-base")
                    )
                    self._ru_accent = (
                        ui.textarea(value=self._sub.ru_accent)
                        .props("rows=2")
                        .classes("w-full text-base")
                    )
            ui.separator()

            ui.label("Voices").classes("text-h5")
            for ogg in self._sub.oggs:
                voices = VoiceBlock(
                    sub_id=self._sub.id,
                    name=ogg.name,
                    ref_text=self._sub.en_sub,
                    target_text=self._sub.ru_accent,
                    ref_audio=ogg.wav_en_path,
                    target_audio=ogg.wav_ru_path,
                )
                self._playlist.add(voices.ru_voice)
            ui.separator()

            with ui.row().classes("items-center"):
                ui.button("💾 Save", on_click=self.save)
                ui.button("🗑 Delete subtitle", on_click=self.dialog().open).props(
                    "color=negative"
                )

    @property
    def playlist(self):
        return self._playlist

    def dialog(self):
        with ui.dialog() as dlg, ui.card():
            ui.label("Delete subtitle?")
            with ui.row():
                ui.button("NO", on_click=dlg.close)
                ui.button(
                    "YES",
                    on_click=lambda: (
                        dlg.close(),
                        self.delete(),
                    ),
                ).props("color=negative")

        return dlg

    def save(self):
        patch_sub(
            sub_id=self._sub.id,
            data=SubPatchDTO(
                ru_sub=self._ru_sub.value,
                ru_accent=self._ru_accent.value,
            ),
        )
        ui.notify("Изменения сохранены", type="positive")

    def delete(self):
        id = self._sub.id

        for ogg in self._sub.oggs:
            VoiceBlock(self._sub, ogg).delete_wav()

        delete_sub(sub_id=id)
        ui.notify("Запись удалена", type="positive")

        self._ids.pop(id)
        ui.navigate.to(f"/subs/{self._ids[self._current_index - 1]}")


class VoiceBlock:
    def __init__(
        self,
        sub_id: int,
        name: str,
        ref_text: str,
        target_text: str,
        ref_audio: str,
        target_audio: str,
    ):
        self._id = sub_id
        self._ref_text = ref_text
        self._target_text = target_text
        self._ref_audio = ref_audio
        self._target_audio = target_audio

        with ui.card().classes("w-full"):
            ui.label(name).classes("text-h6")
            ui.separator()

            ui.label("English")
            if Path(self._ref_audio).exists():
                ui.audio(self._ref_audio).classes("w-full")

            ui.label("Russian")
            with ui.row().classes("w-full items-center"):
                self._ru_voice = ui.audio(self._target_audio).classes("flex-grow")

                self.btn_del_ru_voice = ui.button(
                    "Delete WAV",
                    on_click=self.delete_wav,
                ).props("color=negative")

                self.btn_render = ui.button(
                    "Render",
                    on_click=self.voice_render,
                ).props("color=green")
                self.spin_render = ui.spinner(size="lg")
                self.spin_render.visible = False

        self.refresh()

    @property
    def ru_voice(self):
        return self._ru_voice

    def refresh(self):
        if Path(self._target_audio).exists():
            self._ru_voice.visible = True
            self.btn_del_ru_voice.visible = True
        else:
            self._ru_voice.visible = False
            self.btn_del_ru_voice.visible = False

    def delete_wav(self):
        file = Path(self._target_audio)
        file.unlink(missing_ok=True)
        ui.notify("File deleted", type="positive")

        self.refresh()

    async def voice_render(self):
        self.delete_wav()
        ui.notify(f"{self._ref_audio = }", type="positive")
        ui.notify(f"{self._target_audio = }", type="positive")

        self.btn_render.disable()
        self.spin_render.visible = True
        try:
            await run.io_bound(
                lambda: convert_audio_with_remote_session(
                    sub_id=self._id,
                    ref_text=self._ref_text,
                    target_text=self._target_text,
                    ref_audio=Path(self._ref_audio),
                    target_audio=Path(self._target_audio),
                )
            )
        except Exception as ex:
            logger.error(f"{type(ex)}: {ex}")
            ui.notify("File not rendered", type="negative")
        else:
            ui.notify("File rendered", type="positive")

        self.btn_render.enable()
        self.spin_render.visible = False
        self.refresh()

    @property
    def playlist(self):
        return self._playlist
