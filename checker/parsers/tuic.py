from urllib.parse import (
    urlparse,
    parse_qs
)

from checker.exceptions import (
    InvalidNodeError
)


def parse(line):

    try:

        u = urlparse(line)

        q = parse_qs(u.query)

    except Exception as e:

        raise InvalidNodeError(str(e))

    node = {

        "name":
        u.fragment or "tuic",

        "type":
        "tuic",

        "server":
        u.hostname,

        "port":
        u.port,

        "uuid":
        u.username,

        "password":
        q.get(
            "password",
            [""]
        )[0],

        "sni":
        q.get(
            "sni",
            [""]
        )[0],

        "alpn":
        q.get(
            "alpn",
            ["h3"]
        )[0]
    }

    cc = q.get(
        "congestion-controller",
        [None]
    )[0]

    if cc:

        node[
            "congestion-controller"
        ] = cc

    return node
