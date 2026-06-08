from dataclasses import dataclass
from typing import List, Optional

from checker.speedtest import (
    SpeedTester,
    SpeedResult
)


@dataclass
class BenchmarkResult:

    node: dict

    success: bool

    delay_ms: float

    speed_mbps: float

    score: float

    error: str = ""


class BenchmarkRunner:

    DEFAULT_DELAY_TARGETS = [

        "https://www.baidu.com",

        "https://www.qq.com",

        "https://www.jd.com"

    ]

    DEFAULT_SPEED_TARGET = (

        "https://speed.cloudflare.com/__down"
    )

    def __init__(

        self,

        worker,

        mixed_port: int,

        delay_targets: Optional[List[str]] = None,

        speed_target: Optional[str] = None

    ):

        self.worker = worker

        self.delay_targets = (

            delay_targets

            or

            self.DEFAULT_DELAY_TARGETS
        )

        self.speed_target = (

            speed_target

            or

            self.DEFAULT_SPEED_TARGET
        )

        self.speedtester = SpeedTester(

            mixed_port=mixed_port
        )

    async def delay_test(

        self,

        node: dict

    ) -> Optional[float]:

        delays = []

        for target in self.delay_targets:

            try:

                result = await self.worker.delay(

                    node,

                    target
                )

                if isinstance(result, dict):

                    delay = result.get("delay")

                    if isinstance(

                        delay,

                        (int, float)

                    ):

                        delays.append(delay)

            except Exception:

                continue

        if not delays:

            return None

        return round(

            sum(delays)

            / len(delays),

            2
        )

    async def speed_test(

        self

    ) -> SpeedResult:

        return await self.speedtester.test(

            self.speed_target,

            size_limit_mb=10,

            timeout_sec=20
        )

    def calc_score(

        self,

        delay_ms: float,

        speed_mbps: float

    ) -> float:

        delay_score = max(

            0,

            100 - delay_ms / 10
        )

        speed_score = min(

            speed_mbps,

            100
        )

        score = (

            delay_score * 0.4

            +

            speed_score * 0.6
        )

        return round(score, 2)

    async def run(

        self,

        node: dict

    ) -> BenchmarkResult:

        try:

            await self.worker.prepare(
                node
            )

            delay = await self.delay_test(
                node
            )

            if delay is None:

                return BenchmarkResult(

                    node=node,

                    success=False,

                    delay_ms=9999,

                    speed_mbps=0,

                    score=0,

                    error="delay test failed"
                )

            speed_result = await (
                self.speed_test()
            )

            if speed_result.success:

                speed = speed_result.speed_mbps

            else:

                speed = 0

            score = self.calc_score(

                delay,

                speed
            )

            return BenchmarkResult(

                node=node,

                success=True,

                delay_ms=delay,

                speed_mbps=speed,

                score=score
            )

        except Exception as e:

            return BenchmarkResult(

                node=node,

                success=False,

                delay_ms=9999,

                speed_mbps=0,

                score=0,

                error=str(e)
            )
