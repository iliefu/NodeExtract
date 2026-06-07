from checker.parsers import (

    vmess,
    vless,
    reality,

    trojan,
    ss,

    hysteria2,
    tuic
)


REGISTRY = {

    "vmess://":
    vmess.parse,

    "vless://":
    vless.parse,

    "reality://":
    reality.parse,

    "trojan://":
    trojan.parse,

    "ss://":
    ss.parse,

    "hy2://":
    hysteria2.parse,

    "hysteria2://":
    hysteria2.parse,

    "tuic://":
    tuic.parse
}
