from urllib.parse import (
    urlparse,
    parse_qs
)

from checker.exceptions import (
    InvalidNodeError
)


def parse(line: str):

    try:

        u = urlparse(line)

        q = parse_qs(u.query)

    except Exception as e:

        raise InvalidNodeError(str(e))

    network = q.get(
        "type",
        ["tcp"]
    )[0]

    node = {

        "name":
        u.fragment or "trojan",

        "type":
        "trojan",

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
            "allowInsecure",
            ["0"]
        )[0] == "1",

        "network":
        network
    }

    if network == "ws":

        node["ws-path"] = q.get(
            "path",
            ["/"]
        )[0]

        host = q.get(
            "host",
            [None]
        )[0]

        if host:

            node["ws-headers"] = {
                "Host": host
            }

    elif network == "grpc":

        node[
            "grpc-service-name"
        ] = q.get(
            "serviceName",
            [""]
        )[0]

    return node
