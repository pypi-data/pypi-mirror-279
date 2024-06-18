from __future__ import annotations

import asyncio
from asyncio import Lock, Queue, Task, sleep
from logging import getLogger
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Unpack

from botops import telegram
from botops.core.client import APIClient, Response
from botops.utils import Cleanup, Loader

if TYPE_CHECKING:
    from .handler import Handler

__all__ = ["BotEngine"]

_R = TypeVar("_R")


class BotEngine(Cleanup):
    def __init__(self, token: str) -> None:
        self._client = APIClient()
        self._is_running = False
        self._retry_later_cond = asyncio.Condition()
        self._get_updates_task: Task[Any] | None = None
        self._dispatch_task: Task[Any] | None = None
        self._url = f"/bot{token}"
        self._id = int(token.split(":")[0])
        self._last_update_id: int | None = None
        self._queue: Queue[telegram.Update | None] = asyncio.Queue(maxsize=100)
        self._handlers: list[Handler] = []
        self._load = Loader()
        self._concurrent_tasks = asyncio.Semaphore(value=30)
        self._logger = getLogger(__name__)

    @property
    def bot_id(self) -> int:
        return self._id

    @property
    def handlers(self) -> list[Handler]:
        return self._handlers

    async def execute(
        self,
        http_method: Literal["POST", "GET"],
        method: telegram.Method,
        result: type[_R],
        /,
        **attrs: Any,
    ) -> _R:
        if self._retry_later_cond.locked():
            await self._retry_later_cond.wait()

        match response := await self._client.request(http_method, self._get_path(method), **attrs):
            case Response(ok=True):
                return self._load(result, response.result)
            case Response(error_code=429, parameters={"retry_after": retry_after}):
                await self._delay_execute(retry_after)
                return await self.execute(http_method, method, result)
            case _:
                raise ValueError(
                    f"Telegram response error! Code {response.error_code}! {response.description}"
                )

    async def _on_startup(self) -> None:
        await self._client.startup()
        await self._start_dispatching_updates()
        await self._start_receiving_updates()

    async def _on_shutdown(self) -> None:
        await self._stop_receiving_updates()
        await self._stop_dispatching_updates()
        await self._client.shutdown()

    async def _start_receiving_updates(self) -> None:
        await (worker_lock := Lock()).acquire()

        async def _get_updates_worker() -> None:
            worker_lock.release()
            while self._is_running:
                await self._get_updates(limit=1, timeout=3)

        self._is_running = True
        self._get_updates_task = asyncio.create_task(_get_updates_worker())

        # Wait worker for start running at the event loop.
        await worker_lock.acquire()

    async def _stop_receiving_updates(self) -> None:
        if self._is_running:
            self._is_running = False

        if self._get_updates_task:
            self._logger.warning("Stopping receiving new updates...")
            await self._get_updates_task

    async def _start_dispatching_updates(self) -> None:
        self._dispatch_task = asyncio.create_task(self._dispatch())

    async def _stop_dispatching_updates(self) -> None:
        if self._dispatch_task:
            await self._queue.put(None)

            self._logger.warning("Waiting for the completion of unfinished handlers...")
            await self._dispatch_task

    def _recalculate_last_update_id(self, update_id: int) -> None:
        self._last_update_id = update_id + 1

    def _skip_updates(self, updates: list[telegram.Update]) -> None:
        if len(updates) > 1:
            self._logger.warning(
                f"Updated queue is full ({self._queue.qsize()})!!! "
                f"Skipped from update_id:{updates[0].update_id} "
                f"to update_id:{updates[-1].update_id} ({len(updates)})."
            )
        else:
            self._logger.warning(
                f"Updated queue is full ({self._queue.qsize()})!!! " f"Skipped {updates[-1]}."
            )

    async def _put_updates_to_queue(self, updates: list[telegram.Update]) -> None:
        for index, update in enumerate(updates):
            if self._queue.full():
                return self._skip_updates(updates[index:])

            await self._queue.put(update)

    async def _get_updates(self, **attrs: Unpack[telegram.GetUpdates]) -> None:
        updates = await self.execute(
            "GET",
            telegram.Method.get_updates,
            list[telegram.Update],
            offset=self._last_update_id,
            **attrs,
        )

        if updates:
            self._recalculate_last_update_id(updates[-1].update_id)
            await self._put_updates_to_queue(updates)

    def _get_path(self, method: telegram.Method) -> str:
        return f"{self._url}/{method}"

    async def _delay_execute(self, after: int) -> None:
        if not self._retry_later_cond.locked():
            async with self._retry_later_cond:
                self._logger.warning(f"Re-try after {after} seconds!")
                await sleep(after)

            self._retry_later_cond.notify_all()
            self._logger.warning(f"Re-trying {after} seconds...")

    async def _get_update_from_queue(self) -> telegram.Update | None:
        await self._concurrent_tasks.acquire()
        return await self._queue.get()

    async def _dispatch(self) -> None:
        while update := await self._get_update_from_queue():
            for number, handler in enumerate(reversed(self._handlers), start=1):
                if update_entity := getattr(update, handler.update_type):
                    task = asyncio.create_task(handler(update_entity), name=handler.name)

                    if not handler.Meta.propagation or number == len(self._handlers):
                        # Mark as done only at last handler.
                        task.add_done_callback(self._done_callback)

                    if not handler.Meta.propagation:
                        break
            else:
                # If no handler is found.
                self._queue.task_done()
                self._logger.warning(f"Alone {update} :(")
        else:
            # On shutdown.
            self._concurrent_tasks.release()
            self._queue.task_done()

        # Wait while tasks will be processed.
        await self._queue.join()

    def _done_callback(self, task: Task | None = None) -> None:
        self._concurrent_tasks.release()
        self._queue.task_done()

        if task is None:
            return

        if task.cancelled():
            self._logger.warning(f"Task {task.get_name()} is cancelled!")
        elif exc := task.exception():
            self._logger.exception(f"Task {task.get_name()} {task.get_stack()}!", exc_info=exc)
        else:
            self._logger.info(f"Task {task.get_name()} successfully finished!")
