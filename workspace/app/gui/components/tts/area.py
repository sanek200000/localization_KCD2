from nicegui import ui, run

from app.api.tts import (
    check_tts_loaded_model,
    check_tts_server_connection,
    get_server_url,
)


class TextareaTTSServer:
    def __init__(self) -> None:
        with ui.row().classes("w-full items-end no-wrap"):
            self._area = (
                ui.textarea(label="TTS server:")
                .classes("flex-grow text-base no-wrap")
                .props("readonly rows=3")
            )
            self.btn = ui.button("", on_click=self.refresh).props(
                "round flat icon=refresh"
            )

        ui.timer(0.1, self.refresh, once=True)

    async def refresh(self):
        url = get_server_url()
        connection = await run.io_bound(check_tts_server_connection)
        model = await run.io_bound(check_tts_loaded_model)

        self._area.value = (
            f"server url: {url}\nconnection: {connection}\nloaded model: {model}"
        )

        self._area.update()

    @property
    def area(self):
        return self._area
