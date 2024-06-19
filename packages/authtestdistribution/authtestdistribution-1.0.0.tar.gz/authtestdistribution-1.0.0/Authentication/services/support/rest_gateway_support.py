import requests


def create_rest_template(proxy):
    session = requests.Session()
    if proxy and proxy.proxy_host:
        session.proxies = {
            'http': f"http://{proxy.proxy_host}:{proxy.proxy_port}",
            'https': f"https://{proxy.proxy_host}:{proxy.proxy_port}"
        }
        if proxy.proxy_username and proxy.proxy_password:
            session.auth = (proxy.proxy_username, proxy.proxy_password)
    return session
