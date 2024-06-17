import logging
import requests
import warnings
import os
from urllib3.exceptions import InsecureRequestWarning
from enum import Enum


class Verb(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PATCH = "PATCH"
    AWS = "AWS"
    COMMENT = "COMMENT"

    def __str__(self):
        return str(self.value)


class CxCaller:
    def __init__(self, domain_name, token):
        self.domain_name = domain_name
        self.token = token

    def call(
        self,
        verb: Verb,
        service: str,
        path: str = "",
        payload: any = None,
        headers: any = None,
    ):
        proxy = None
        if headers == None:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        proxy_url = os.environ.get("PROXY")
        if proxy_url:
            proxy = {"http": proxy_url, "https": proxy_url}

        url = f"https://{service}.{self.domain_name}/{path}"
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=InsecureRequestWarning)
            logging.debug(f"Calling {verb} {url}")
            x = None
            if verb == Verb.GET:
                x = requests.get(url, proxies=proxy, verify=False, headers=headers)
            elif verb == Verb.DELETE:
                x = requests.delete(url, proxies=proxy, verify=False, headers=headers)
                x.raise_for_status()
                return {}
            elif verb == Verb.POST:
                x = requests.post(
                    url, json=payload, proxies=proxy, verify=False, headers=headers
                )
            elif verb == Verb.PATCH:
                x = requests.patch(
                    url, json=payload, proxies=proxy, verify=False, headers=headers
                )
            else:
                raise Exception(f"Verb {verb} not supported in call_dbs")
            x.raise_for_status()
            return x.json()
