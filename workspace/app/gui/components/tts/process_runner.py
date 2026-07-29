import asyncio
import sys
from typing import Optional

from loguru import logger
from nicegui import run, ui

from app.utils.tts import check_ready_tts_server


class ProcessRunner:
    def __init__(self, module: str, *args: str, max_lines: int = 1000) -> None:
        self.module = module
        self.args = args

        self.process: Optional[asyncio.subprocess.Process] = None
        self._render_task: Optional[asyncio.Task] = None
        self._running = False

        with ui.row().classes("w-full no-wrap items-start") as self.root:
            with ui.column().classes("items-stretch"):
                self.btn_start = ui.button("start", on_click=self.start, color="green")

                self.btn_stop = ui.button("stop", on_click=self.stop, color="red")
                self.btn_stop.disable()

            self.log = ui.log(max_lines=max_lines).classes("w-full h-200")

    async def refresh(self):
        check = await run.io_bound(check_ready_tts_server)
        self.root.set_visibility(check)

    async def start(self):
        if self._running:
            return

        self.log.clear()

        command = [
            sys.executable,
            "-u",
            "-m",
            self.module,
            *self.args,
        ]

        self._running = True
        self.process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        self.btn_start.disable()
        self.btn_stop.enable()

        self._render_task = asyncio.create_task(self._read_stdout())

    async def stop(self):
        if not self.process:
            return

        self.process.terminate()

        try:
            await asyncio.wait_for(self.process.wait(), timeout=3)
        except asyncio.TimeoutError:
            self.process.kill()
            await self.process.wait()

        if self._render_task:
            await self._render_task

        self._running = False
        self.process = None

        self.btn_start.enable()
        self.btn_stop.disable()

    async def _read_stdout(self):
        assert self.process
        assert self.process.stdout

        buffer: list[str] = list()

        while True:
            line = await self.process.stdout.readline()

            if not line:
                break

            buffer.append(line.decode(encoding="utf-8", errors="replace").rstrip())

            if len(buffer) >= 20:
                self.log.push("\n".join(buffer))
                buffer.clear()

        if buffer:
            self.log.push("\n".join(buffer))

        await self.process.wait()

        self._running = False
        self.process = None

        self.btn_start.enable()
        self.btn_stop.disable()
