from nicegui import ui


def create_header():
    with ui.header(elevated=True).classes("items-center justufy-between"):
        ui.label("Kingdom Come Deliverance II locaslization").classes("text-h6")
        ui.label("NiceGUI")
