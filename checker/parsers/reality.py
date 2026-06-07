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
        u.fragment or "reality",

        "type":
        "vless",

        "server":
        u.hostname,

        "port":
        u.port,

        "uuid":
        u.username,

        "network":
        q.get(
            "type",
            ["tcp"]
        )[0],

        "tls":
        True,

        "reality-opts": {

            "public-key":
            q.get(
                "pbk",
                [""]
            )[0],

            "short-id":
            q.get(
                "sid",
                [""]
            )[0]
        }
    }

    fp = q.get(
        "fp",
        [None]
    )[0]

    if fp:

        node[
            "client-fingerprint"
        ] = fp

    sni = q.get(
        "sni",
        [None]
    )[0]

    if sni:

        node[
            "servername"
        ] = sni

    return node
