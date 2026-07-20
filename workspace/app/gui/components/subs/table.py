from collections.abc import Callable

from nicegui import ui


class SubsTable:
    def __init__(self, on_open: Callable[[int], None]) -> None:
        self.grid = ui.aggrid(
            {
                "columnDefs": [
                    {
                        "field": "id",
                        "width": 90,
                    },
                    {
                        "field": "key",
                        "width": 180,
                    },
                    {
                        "field": "en_sub",
                        "flex": 2,
                    },
                    {
                        "field": "ru_sub",
                        "flex": 2,
                    },
                    {
                        "field": "accent",
                        "flex": 2,
                    },
                    {
                        "field": "en_audio",
                        "width": 80,
                    },
                    {
                        "field": "ru_audio",
                        "width": 80,
                    },
                ],
                "rowData": [],
                "pagination": True,
                "paginationPageSize": 100,
                "domLayout": "normal",
            }
        ).classes("w-full ")  # TODO: add h-full

        self.grid.on("cellDubleClicked", lambda e: on_open(e.args["data"]["id"]))

    def set_rows(self, rows):
        self.grid.options["rowData"] = rows
        self.grid.update()
