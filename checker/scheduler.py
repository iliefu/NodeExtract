import asyncio

from checker.worker_pool import (
    WorkerPool
)

from checker.benchmark import (
    run
)


class Scheduler:

    def __init__(

        self,

        workers,

        concurrency=50
    ):

        self.pool = WorkerPool(
            workers
        )

        self.sem = asyncio.Semaphore(
            concurrency
        )

    async def task(

        self,

        node
    ):

        async with self.sem:

            worker = self.pool.acquire()

            return await run(

                worker,

                node
            )

    async def dispatch(

        self,

        nodes
    ):

        return await asyncio.gather(

            *[
                self.task(x)

                for x in nodes
            ]
        )
