from checker.subscription import (
    fetch
)

from checker.dispatcher import (
    dispatch
)

from checker.scheduler import (
    Scheduler
)

import asyncio


lines = fetch(SUB_URL)

nodes = []

for line in lines:

    r = dispatch(line)

    if r.ok:

        nodes.append(r.node)


scheduler = Scheduler(

    workers=[

        "http://mihomo1:9090",

        "http://mihomo2:9090",

        "http://mihomo3:9090"
    ]
)


results = asyncio.run(

    scheduler.dispatch(
        nodes
    )
)
