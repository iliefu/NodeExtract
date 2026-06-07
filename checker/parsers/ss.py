import base64

from urllib.parse import (
    urlparse,
    parse_qs,
    unquote
)

from checker.exceptions import (
    InvalidNodeError
)


SUPPORTED_CIPHERS = {

    "aes-128-gcm",
    "aes-256-gcm",
    "chacha20-ietf-poly1305",
    "2022-blake3-aes-128-gcm",
    "2022-blake3-aes-256-gcm"
}


def decode_userinfo(raw):

    padding = "=" * (
        -len(raw) % 4
    )

    decoded = base64.b64decode(
        raw + padding
    ).decode()

    return decoded.split(
        ":",
        1
    )


def parse(line):

    try:

        body = line[5:]

        if "#" in body:

            body, frag = body.split(
                "#",
                1
            )

            name = unquote(frag)

        else:

            name = "ss"

        parsed = urlparse(
            "ss://" + body
        )

    except Exception as e:

        raise InvalidNodeError(str(e))

    if parsed.username:

        cipher = parsed.username

        password = parsed.password

    else:

        userinfo = (
            parsed.netloc
            .split("@")[0]
        )

        cipher, password = (
            decode_userinfo(
                userinfo
            )
        )

    node = {

        "name":
        name,

        "type":
        "ss",

        "server":
        parsed.hostname,

        "port":
        parsed.port,

        "cipher":
        cipher,

        "password":
        password
    }

    q = parse_qs(parsed.query)

    plugin = q.get(
        "plugin",
        [None]
    )[0]

    if plugin:

        node["plugin"] = plugin

    return node
