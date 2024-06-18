from __future__ import annotations

import asyncio
import signal
from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from botops import Bot


async def run(*bots: Bot) -> None:
    logger = getLogger(__name__)
    async with (lock := asyncio.Lock()):
        loop = asyncio.get_running_loop()

        def shutdown(s: signal.Signals) -> None:
            logger.warning(f"Shutting down by {s.name}:{s.value}...")
            lock.release()

        for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, shutdown, sig)

        try:
            logger.info("Starting up...")
            await asyncio.gather(*(bot.startup() for bot in bots))
            logger.info("Running...")
            await lock.acquire()
        finally:
            await asyncio.gather(*(bot.shutdown() for bot in bots))
