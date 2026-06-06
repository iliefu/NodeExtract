import base64
from urllib.parse import (
    urlparse,
    parse_qs,
    unquote
)

from checker.exceptions import (
    MissingFieldError
)


def b64decode_auto(data: str) -> bytes:

    padding = "=" * (-len(data) % 4)

    return base64.b64decode(
        data + padding
    )


def parse_query(url: str) -> dict:

    parsed = urlparse(url)

    q = parse_qs(parsed.query)

    return {
        k: v[0]
        for k, v in q.items()
    }


def parse_name(url: str) -> str:

    parsed = urlparse(url)

    if parsed.fragment:

        return unquote(parsed.fragment)

    return ""


def require(
    data: dict,
    field: str
):

    if field not in data:

        raise MissingFieldError(
            f"{field} required"
        )

    return data[field]


def boolify(v):

    if isinstance(v, bool):
        return v

    return str(v).lower() in (
        "1",
        "true",
        "yes"
    )
