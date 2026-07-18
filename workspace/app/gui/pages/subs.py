from nicegui import ui

from app.gui.layout import page_layaut


def subs_page():
    def content():
        ui.label("Subtitles").classes("text-h4")

        search = ui.input(
            label="Search",
            placeholder="Enter text...",
        ).classes("w-full")

        grid = ui.aggrid(
            {
                "columnDefs": [
                    {
                        "field": "id",
                        "width": 90,
                    },
                    {
                        "field": "en_sub",
                        "flex": 3,
                    },
                    {
                        "field": "ru_sub",
                        "flex": 3,
                    },
                    {
                        "field": "ru_accent",
                        "flex": 3,
                    },
                ],
                "rowData": [],
                "pagination": True,
                "paginationPageSize": 100,
                "animateRows": True,
            }
        ).classes("w-full")

        async def load():
            rows = list()
            grid.options["rowData"] = rows
            grid.update()

        ui.button("Refresh", on_click=load)

    page_layaut(content)
