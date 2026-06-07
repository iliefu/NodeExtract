import aiohttp
import yaml


class MihomoClient:

    def __init__(
        self,
        controller
    ):

        self.controller = controller

    async def push_config(
        self,
        node
    ):

        payload = {

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

        async with aiohttp.ClientSession() as s:

            await s.put(

                f"{self.controller}/configs",

                json={
                    "payload":
                    yaml.safe_dump(
                        payload,
                        sort_keys=False
                    )
                }
            )

    async def delay(
        self,
        proxy,
        target,
        timeout=5000
    ):

        async with aiohttp.ClientSession() as s:

            async with s.get(

                f"{self.controller}/proxies/{proxy}/delay",

                params={

                    "url":
                    target,

                    "timeout":
                    timeout
                }

            ) as r:

                return await r.json()
