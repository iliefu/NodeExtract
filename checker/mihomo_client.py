import aiohttp
import yaml


class MihomoClient:

    def __init__(
        self,
        controller_url: str,
        secret: str = ""
    ):

        self.controller_url = controller_url.rstrip("/")

        self.secret = secret

    def headers(self):

        if not self.secret:

            return {}

        return {

            "Authorization":
            f"Bearer {self.secret}"
        }

    async def reload_config(

        self,

        node: dict
    ):

        cfg = {

            "mixed-port": 7890,

            "mode": "rule",

            "log-level": "silent",

            "proxies": [

                node
            ],

            "proxy-groups": [

                {
                    "name":
                    "AUTO",

                    "type":
                    "select",

                    "proxies": [

                        node["name"]
                    ]
                }
            ],

            "rules": [

                "MATCH,AUTO"
            ]
        }

        payload = yaml.safe_dump(

            cfg,

            allow_unicode=True,

            sort_keys=False
        )

        async with aiohttp.ClientSession() as s:

            async with s.put(

                f"{self.controller_url}/configs",

                headers=self.headers(),

                json={

                    "payload":
                    payload
                }

            ) as r:

                return await r.text()

    async def health_check(self):

        async with aiohttp.ClientSession() as s:

            async with s.get(

                f"{self.controller_url}/version",

                headers=self.headers()

            ) as r:

                return r.status == 200

    async def proxy_delay(

        self,

        proxy_name,

        url,

        timeout=5000
    ):

        async with aiohttp.ClientSession() as s:

            async with s.get(

                f"{self.controller_url}/proxies/{proxy_name}/delay",

                headers=self.headers(),

                params={

                    "url": url,

                    "timeout": timeout
                }

            ) as r:

                return await r.json()
