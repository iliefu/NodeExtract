import base64
import requests


def fetch(url):

    text = requests.get(

        url,

        timeout=30

    ).text.strip()

    try:

        text = base64.b64decode(

            text + "==="

        ).decode()

    except:

        pass

    return [

        x.strip()

        for x in text.splitlines()

        if x.strip()
    ]
