from __future__ import annotations

from collections.abc import Callable, Hashable
from typing import TYPE_CHECKING, Unpack

from botops import telegram
from botops.core.engine import BotEngine
from botops.triggers import And, Cron, Date, Interval, Or
from botops.utils import Cleanup, Scheduler

if TYPE_CHECKING:
    from .handler import Handler

__all__ = ["Bot"]


class Bot(Cleanup):
    def __init__(self, token: str) -> None:
        self._engine = BotEngine(token)
        self._scheduler = Scheduler()

    def schedule(
        self,
        job_id: Hashable,
        /,
        job: Callable,
        trigger: And | Or | Interval | Cron | Date,
    ) -> None:
        self.unschedule(job_id)
        self._scheduler.add_job(job, trigger, id=str(hash(job_id)))

    def unschedule(self, job_id: Hashable, /) -> None:
        if job := self._scheduler.get_job(str(hash(job_id))):
            job.remove()

    def register_handler(self, *handlers: type[Handler]) -> None:
        self._engine.handlers.extend(handler(self) for handler in handlers)

    async def _on_startup(self) -> None:
        await self._engine.startup()

        if not self._scheduler.running:
            self._scheduler.start()

    async def _on_shutdown(self) -> None:
        if self._scheduler.running:
            self._scheduler.shutdown(wait=True)

        await self._engine.shutdown()

    async def get_me(self) -> telegram.User:
        return await self._engine.execute("GET", telegram.Method.get_me, telegram.User)

    async def log_out(self) -> bool:
        return await self._engine.execute("GET", telegram.Method.log_out, bool)

    async def close(self) -> bool:
        return await self._engine.execute("GET", telegram.Method.close, bool)

    async def send_message(self, **attrs: Unpack[telegram.SendMessage]) -> telegram.Message:
        return await self._engine.execute(
            "POST", telegram.Method.send_message, telegram.Message, **attrs
        )
