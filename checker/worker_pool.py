import asyncio
from typing import List, Union

from checker.worker import Worker


class WorkerPool:
    """
    管理多个 Worker，实现轮询分配。
    每个 Worker 对应一个 Mihomo 实例，避免配置覆盖。
    """
    def __init__(
        self,
        workers: Union[List[str], List[Worker]],
        secrets: List[str] = None
    ):
        """
        初始化 WorkerPool
        
        Args:
            workers: Worker 对象列表或 Mihomo 控制器 URL 列表
            secrets: 对应的 Mihomo 访问令牌列表 (可选)
        """
        # 如果传入的是URL列表，转换为Worker对象
        if workers and isinstance(workers[0], str):
            self.workers = []
            for i, url in enumerate(workers):
                secret = (secrets[i] if secrets and i < len(secrets) else "")
                self.workers.append(
                    Worker(
                        worker_id=i,
                        controller=url,
                        secret=secret
                    )
                )
        else:
            # 传入的已经是Worker对象列表
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
        """
        获取 Worker 池大小
        """
        return len(self.workers)
