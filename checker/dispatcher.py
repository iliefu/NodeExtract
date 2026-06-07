from checker.parser import (
    parse_node
)

from checker.validator import (
    validate
)

from checker.normalizer import (
    normalize
)


class DispatchResult:

    def __init__(
        self,
        ok,
        node=None,
        error=None
    ):

        self.ok = ok
        self.node = node
        self.error = error


def dispatch(
    line: str
):

    try:

        node = parse_node(
            line
        )

        node = normalize(
            node
        )

        if not validate(
            node
        ):

            return DispatchResult(

                ok=False,

                error="validation failed"
            )

        return DispatchResult(

            ok=True,

            node=node
        )

    except Exception as e:

        return DispatchResult(

            ok=False,

            error=str(e)
        )
