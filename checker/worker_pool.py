from checker.mihomo_client import (
    MihomoClient
)


class WorkerPool:

    def __init__(
        self,
        workers
    ):

        self.workers = [

            MihomoClient(x)

            for x in workers
        ]

        self.idx = 0

    def acquire(self):

        worker = self.workers[
            self.idx
        ]

        self.idx += 1

        self.idx %= len(
            self.workers
        )

        return worker
