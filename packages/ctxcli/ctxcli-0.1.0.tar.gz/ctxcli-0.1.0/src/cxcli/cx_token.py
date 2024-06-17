import requests
import json
import os
from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=2, ttl=3600))
def get_token(username, password, tenant, dbs_domain_name): 
    proxy_url = os.getenv("PROXY")
    proxy = None
    if (proxy_url):
        proxy = {
            'http': proxy_url,
            'https': proxy_url
        }
    url = f"https://cognito.{dbs_domain_name}/auth/initiate"
    payload = {
        "Username": username,
        "Password": password, 
        "TenantName": tenant,
        "ApplicationClient": "catalog"
        }
    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=payload, verify=False, proxies=proxy)
    response.raise_for_status()

    TOKEN = (response.json()['AccessToken'])
        
    return TOKEN