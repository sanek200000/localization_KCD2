import asyncio
from typing import Optional

from nicegui import ui


class ProcessLog:
    def __init__(
        self,
        max_lines: int = 1000,
        flush_interval: float = 1.0,
        height: int = 180,
    ) -> None:
        self._buffer: list[str] = list()
        self._task: Optional[asyncio.Task] = None
        self._running = False
        self._flush_interval = flush_interval

        self.log = ui.log(max_lines=max_lines).classes(f"w-full h-{height}")

    def write(self, text: str):
        self._buffer.append(text)

    async def start(self):
        if self._running:
            return

        self.log.clear()

        self._running = True
        self._task = asyncio.create_task(self._flush())

    async def stop(self):
        self._running = False

        if self._task:
            await self._task

    async def _flush(self):
        while self._running or self._buffer:
            if self._buffer:
                self.log.push("\n".join(self._buffer))
                self._buffer.clear()

            await asyncio.sleep(self._flush_interval)
