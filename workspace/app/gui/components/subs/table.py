from collections.abc import Callable

from nicegui import ui


class SubsTable:
    def __init__(self, on_open: Callable[[int], None]) -> None:
        self.grid = ui.aggrid(
            {
                "columnDefs": [
                    {
                        "headerName": "id",
                        "field": "id",
                        "width": 60,
                    },
                    {
                        "headerName": "key",
                        "field": "key",
                        "width": 180,
                    },
                    {
                        "headerName": "English",
                        "field": "en_sub",
                        "flex": 2,
                    },
                    {
                        "headerName": "Russian",
                        "field": "ru_sub",
                        "flex": 2,
                    },
                    {
                        "field": "accent",
                        "flex": 2,
                    },
                    {
                        "headerName": "Audio count",
                        "field": "audio_count",
                        "width": 80,
                    },
                ],
                "rowData": [],
                "animateRows": False,
                "pagination": False,
                "domLayout": "autoHeight",
                "rowSelection": "single",
            }
        )

        self.grid.classes("w-full flex-grow h-full")
        # self.grid.style("height: unset")
        self.grid.on("cellDoubleClicked", lambda e: on_open(e.args["data"]["id"]))
        self.grid.on(
            "cellDoubleClicked", lambda e: ui.notify(str(e.args["data"]["id"]))
        )

    def set_rows(self, rows):
        self.grid.options["rowData"] = rows
        self.grid.update()
