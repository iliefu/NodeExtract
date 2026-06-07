QQ204 = (

    "http://www.qq.com"

    "/generate_204"
)

BAIDU = (

    "https://www.baidu.com"
)
from checker.models import (
    BenchmarkResult
)


async def run(
    worker,
    node
):

    await worker.push_config(
        node
    )

    result = await worker.delay(

        node["name"],

        QQ204
    )

    delay = result.get(
        "delay",
        9999
    )

    return BenchmarkResult(

        node=node,

        delay=delay,

        speed=0,

        success=delay < 3000
    )
