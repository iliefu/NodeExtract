from checker.registry import (
    REGISTRY
)

from checker.exceptions import (
    UnsupportedProtocolError
)


def parse_node(
    line: str
):

    line = line.strip()

    for prefix, fn in REGISTRY.items():

        if line.startswith(prefix):

            return fn(line)

    raise UnsupportedProtocolError(
        line[:64]
    )
