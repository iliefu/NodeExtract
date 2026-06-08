import asyncio

from checker.mihomo_client import (
    MihomoClient
)


class Worker:

    def __init__(

        self,

        worker_id,

        controller,

        secret=""
    ):

        self.worker_id = worker_id

        self.client = MihomoClient(

            controller,

            secret
        )

        self.lock = asyncio.Lock()

    async def prepare(

        self,

        node
    ):

        async with self.lock:

            await self.client.reload_config(
                node
            )

            await asyncio.sleep(1)

    async def delay(

        self,

        node,

        target
    ):

        async with self.lock:

            result = await (

                self.client.proxy_delay(

                    node["name"],

                    target
                )
            )

            return result

    async def benchmark(

        self,

        node,

        target
    ):

        async with self.lock:

            await self.prepare(node)

            result = await self.delay(

                node,

                target
            )

            return result
