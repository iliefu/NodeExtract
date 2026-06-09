import asyncio
from typing import List
from checker.worker_pool import WorkerPool
from checker.benchmark import BenchmarkRunner, BenchmarkResult

class Scheduler:
    """
    并发调度节点测速。
    """
    def __init__(
        self,
        workers: List,
        concurrency: int = 50,
        mixed_port: int = 7890
    ):
        """
        workers: Worker 对象列表
        concurrency: 最大并发数
        mixed_port: Mihomo mixed-port 用于速度测试
        """
        self.pool = WorkerPool(workers)
        self.sem = asyncio.Semaphore(concurrency)
        self.mixed_port = mixed_port

    async def task(self, node: dict) -> BenchmarkResult:
        """
        单节点测速任务
        """
        async with self.sem:
            worker = await self.pool.acquire()
            runner = BenchmarkRunner(worker, mixed_port=self.mixed_port)
            result = await runner.run(node)
            return result

    async def dispatch(self, nodes: List[dict]) -> List[BenchmarkResult]:
        """
        批量调度节点测速
        """
        tasks = [self.task(node) for node in nodes]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results
