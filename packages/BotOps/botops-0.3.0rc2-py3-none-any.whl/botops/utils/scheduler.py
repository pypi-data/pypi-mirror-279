from apscheduler.schedulers.asyncio import AsyncIOScheduler

__all__ = ["Scheduler"]


class Scheduler(AsyncIOScheduler):
    def __init__(self) -> None:
        super().__init__(job_defaults=dict(coalesce=True))
