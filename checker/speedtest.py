import aiohttp
import asyncio
import time
from dataclasses import dataclass


@dataclass
class SpeedResult:

    success: bool

    speed_mbps: float

    bytes_read: int

    elapsed: float

    error: str = ""


class SpeedTester:

    def __init__(

        self,

        mixed_port: int,

        host: str = "127.0.0.1"
    ):

        self.proxy = (

            f"http://{host}:{mixed_port}"
        )

    async def test(

        self,

        url: str,

        size_limit_mb: int = 10,

        timeout_sec: int = 20
    ):

        limit = (

            size_limit_mb

            * 1024

            * 1024
        )

        total = 0

        start = time.time()

        timeout = aiohttp.ClientTimeout(

            total=timeout_sec
        )

        try:

            async with aiohttp.ClientSession(

                timeout=timeout

            ) as session:

                async with session.get(

                    url,

                    proxy=self.proxy

                ) as resp:

                    async for chunk in (

                        resp.content.iter_chunked(

                            65536
                        )
                    ):

                        total += len(chunk)

                        if total >= limit:

                            break

            elapsed = max(

                time.time() - start,

                0.001
            )

            mbps = (

                total * 8

            ) / (

                elapsed * 1024 * 1024
            )

            return SpeedResult(

                success=True,

                speed_mbps=round(
                    mbps,
                    2
                ),

                bytes_read=total,

                elapsed=elapsed
            )

        except Exception as e:

            return SpeedResult(

                success=False,

                speed_mbps=0,

                bytes_read=0,

                elapsed=0,

                error=str(e)
            )
