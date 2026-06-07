from dataclasses import dataclass


@dataclass
class NodeTask:

    node: dict


@dataclass
class BenchmarkResult:

    node: dict

    delay: float

    speed: float

    success: bool
