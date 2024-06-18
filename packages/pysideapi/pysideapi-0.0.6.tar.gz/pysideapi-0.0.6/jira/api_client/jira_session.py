import requests
import json


def get_basic_session(url_session=None, username=None, token=None, proxy=False):
    session = requests.Session()
    payload = json.dumps({
        "username": username,
        "password": token
    })
    headers = {
        'Content-Type': 'application/json'
    }
    current_proxies = {
        'https': 'http://118.180.54.170:8080',
        'http': 'http://118.180.54.170:8080'
    }

    if not proxy:
        r = session.post(url_session, headers=headers, data=payload)
    else:
        r = session.post(url_session, headers=headers, data=payload, proxies=current_proxies)

    cookies = requests.utils.dict_from_cookiejar(r.cookies)
    print(json.loads(r.text))
    session.cookies.update(cookies)
    session.headers.update(headers)

    if not proxy:
        session.proxies.update({})
    else:
        session.proxies.update(current_proxies)

    return session


