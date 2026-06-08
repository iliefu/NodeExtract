from dataclasses import dataclass

from checker.speedtest import (

    SpeedTester
)


@dataclass
class BenchmarkResult:

    node: dict

    success: bool

    delay_ms: float

    speed_mbps: float

    score: float

    error: str = ""
