from nicegui import ui


def create_sidebar() -> None:
    ui.button(
        "🏠 Dashboard",
        on_click=lambda: ui.navigate.to("/"),
    ).props("flat").classes("w-full justify-start")

    ui.button(
        "📝 Subtitles",
        on_click=lambda: ui.navigate.to("/subs"),
    ).props("flat").classes("w-full justify-start")

    ui.button(
        "🎵 OGG",
        on_click=lambda: ui.navigate.to("/oggs"),
    ).props("flat").classes("w-full justify-start")

    ui.button(
        "🗣 TTS",
        on_click=lambda: ui.navigate.to("/tts"),
    ).props("flat").classes("w-full justify-start")

    ui.button(
        "⚙ Settings",
        on_click=lambda: ui.navigate.to("/settings"),
    ).props("flat").classes("w-full justify-start")
