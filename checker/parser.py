from checker.parsers import (
    vmess,
    vless,
    reality,
    trojan,
    ss,
    hysteria2,
    tuic
)

from checker.exceptions import (
    UnsupportedProtocolError
)


def parse_node(
    line: str
):

    line = line.strip()

    if not line:
        raise UnsupportedProtocolError(
            "empty line"
        )

    if line.startswith("vmess://"):
        return vmess.parse(line)

    if line.startswith("vless://"):
        return vless.parse(line)

    if line.startswith("trojan://"):
        return trojan.parse(line)

    if line.startswith("ss://"):
        return ss.parse(line)

    if line.startswith("hy2://"):
        return hysteria2.parse(line)

    if line.startswith("hysteria2://"):
        return hysteria2.parse(line)

    if line.startswith("tuic://"):
        return tuic.parse(line)

    if line.startswith("reality://"):
        return reality.parse(line)

    raise UnsupportedProtocolError(
        line[:32]
    )
