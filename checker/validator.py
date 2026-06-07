REQUIRED = {

    "vmess": [
        "server",
        "port",
        "uuid"
    ],

    "vless": [
        "server",
        "port",
        "uuid"
    ],

    "trojan": [
        "server",
        "port",
        "password"
    ],

    "ss": [
        "server",
        "port",
        "cipher",
        "password"
    ],

    "hysteria2": [
        "server",
        "port",
        "password"
    ],

    "tuic": [
        "server",
        "port",
        "uuid"
    ]
}


def validate(node):

    typ = node["type"]

    for field in REQUIRED.get(
        typ,
        []
    ):

        if not node.get(field):

            return False

    return True
