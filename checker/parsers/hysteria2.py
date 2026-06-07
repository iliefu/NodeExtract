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
        u.fragment or "hy2",

        "type":
        "hysteria2",

        "server":
        u.hostname,

        "port":
        u.port,

        "password":
        u.username,

        "sni":
        q.get(
            "sni",
            [""]
        )[0],

        "skip-cert-verify":
        q.get(
            "insecure",
            ["0"]
        )[0] == "1"
    }

    obfs = q.get(
        "obfs",
        [None]
    )[0]

    if obfs:

        node["obfs"] = obfs

        node["obfs-password"] = (
            q.get(
                "obfs-password",
                [""]
            )[0]
        )

    return node
