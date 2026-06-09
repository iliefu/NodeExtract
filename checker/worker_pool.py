import asyncio
from typing import List
from checker.worker import Worker

class WorkerPool:
    """
    管理多个 Worker，实现轮询分配。
    每个 Worker 对应一个 Mihomo 实例，避免配置覆盖。
    """
    def __init__(self, workers: List[Worker]):
        self.workers = workers
        self.idx = 0
        self.lock = asyncio.Lock()

    async def acquire(self) -> Worker:
        """
        轮询获取一个 Worker。
        """
        async with self.lock:
            worker = self.workers[self.idx]
            self.idx += 1
            self.idx %= len(self.workers)
            return worker

    async def size(self) -> int:
        return len(self.workers)
