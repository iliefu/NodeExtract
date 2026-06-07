from urllib.parse import (
    urlparse,
    parse_qs
)

from checker.exceptions import (
    InvalidNodeError
)


def parse(
    line: str
):

    try:

        u = urlparse(line)

        q = parse_qs(
            u.query
        )

    except Exception as e:

        raise InvalidNodeError(
            str(e)
        )

    node = {

        "name":
        u.fragment or "vless",

        "type":
        "vless",

        "server":
        u.hostname,

        "port":
        u.port,

        "uuid":
        u.username,

        "tls":
        q.get(
            "security",
            ["none"]
        )[0]
        in (
            "tls",
            "reality"
        ),

        "network":
        q.get(
            "type",
            ["tcp"]
        )[0]
    }

    flow = q.get(
        "flow",
        [None]
    )[0]

    if flow:

        node["flow"] = flow

    sni = q.get(
        "sni",
        [None]
    )[0]

    if sni:

        node["servername"] = sni

    path = q.get(
        "path",
        [None]
    )[0]

    if path:

        node["ws-path"] = path

    return node
