from collections.abc import Callable

from nicegui import ui
from math import ceil


class Pager:
    def __init__(
        self, *, page_size: int = 100, on_change: Callable[[int, int], None]
    ) -> None:
        self.page = 0
        self.page_size = page_size
        self.total = 0
        self.on_change = on_change

        with ui.row().classes("items-center gap-2"):
            self.first_btn = ui.button("<<", on_click=self.first)
            self.prev_btn = ui.button("<", on_click=self.prev)

            self.lable = ui.label()

            self.next_btn = ui.button(">", on_click=self.next)
            self.last_btn = ui.button(">>", on_click=self.last)

    def set_total(self, total: int):
        self.total = total
        self.refresh()

    @property
    def pages(self):
        return max(ceil(self.total / self.page_size), 1)

    def refresh(self):
        self.lable.text = f"Page {self.page + 1} / {self.pages} (of {self.total})"

        self.prev_btn.enabled = self.page > 0
        self.first_btn.enabled = self.page > 0

        self.next_btn.enabled = self.page < self.pages - 1
        self.last_btn.enabled = self.page < self.pages - 1

    def emit(self):
        self.refresh()
        self.on_change(self.page * self.page_size, self.page_size)

    def first(self):
        self.page = 0
        self.emit()

    def prev(self):
        if self.page:
            self.page -= 1
            self.emit()

    def next(self):
        if self.page < self.pages - 1:
            self.page += 1
            self.emit()

    def last(self):
        self.page = self.pages - 1
        self.emit()
