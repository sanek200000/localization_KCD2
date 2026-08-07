import sys
import asyncio
from typing import Optional

from loguru import logger

from app.gui.components.log_window import ProcessLog


class ProcessController:
    def __init__(self, module: str, log: ProcessLog) -> None:
        self._module = module
        self._log = log

        self.process: Optional[asyncio.subprocess.Process] = None
        self._render_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self, *args):
        if self._running:
            return

        command = [sys.executable, "-u", "-m", self._module, *args]
        logger.info(f"Start command: {' '.join(command)}")

        await self._log.start()

        self._running = True
        self.process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

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

    async def _read_stdout(self):
        assert self.process
        assert self.process.stdout

        while True:
            line = await self.process.stdout.readline()
            if not line:
                break

            self._log.write(
                line.decode(
                    encoding="utf-8",
                    errors="replace",
                ).rstrip()
            )

        await self.process.wait()

        self._running = False
        self.process = None

        await self._log.stop()
