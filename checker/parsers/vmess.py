import json

from checker.parsers.base import (
    b64decode_auto
)

from checker.exceptions import (
    InvalidNodeError
)


def parse(
    line: str
):

    try:

        raw = line[8:]

        payload = b64decode_auto(
            raw
        )

        data = json.loads(
            payload
        )

    except Exception as e:

        raise InvalidNodeError(
            f"vmess decode failed: {e}"
        )

    node = {

        "name":
        data.get(
            "ps",
            "vmess"
        ),

        "type":
        "vmess",

        "server":
        data["add"],

        "port":
        int(data["port"]),

        "uuid":
        data["id"],

        "alterId":
        int(
            data.get(
                "aid",
                0
            )
        ),

        "cipher":
        data.get(
            "scy",
            "auto"
        ),

        "tls":
        data.get(
            "tls"
        ) == "tls",

        "network":
        data.get(
            "net",
            "tcp"
        )
    }

    host = data.get("host")

    path = data.get("path")

    if path:

        node["ws-path"] = path

    if host:

        node["ws-headers"] = {
            "Host": host
        }

    if data.get("sni"):

        node["servername"] = (
            data["sni"]
        )

    if data.get("alpn"):

        node["alpn"] = (
            data["alpn"]
            .split(",")
        )

    return node
