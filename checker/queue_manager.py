import asyncio


class QueueManager:

    def __init__(self):

        self.queue = asyncio.Queue()

    async def put(self, task):

        await self.queue.put(task)

    async def get(self):

        return await self.queue.get()

    def size(self):

        return self.queue.qsize()
