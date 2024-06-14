from typing import Dict, Optional
from requests import Session

from .utils import RequestsAdapter, Retry, ProxyParams
from ..Utils import version

class requests:

    def __new__(cls, timeout: int = 15, extra_headers: Dict[str, str] = dict(), proxyParams: Optional[ProxyParams] = None) -> 'Session':
        if not proxyParams: proxy_url = None
        else: proxy_url = proxyParams.URL
        requests = Session()
        adapter = RequestsAdapter(timeout=timeout, max_retries=Retry)
        for scheme in ('http://', 'https://'): requests.mount(scheme, adapter)
        if not proxy_url:
            requests.proxies = dict()
        else:
            requests.proxies = dict(http = proxy_url, https = proxy_url)

        header: Dict[str, str] = dict()
        try:
            for k, v in zip(extra_headers.keys(), extra_headers.values()): header.update(**{k.lower():v})
            if not header.get('User-Agent'.lower()):
                header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        except AttributeError:
            if not header.get('User-Agent'.lower()):
                header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        requests.headers.update(**header)
        return requests
