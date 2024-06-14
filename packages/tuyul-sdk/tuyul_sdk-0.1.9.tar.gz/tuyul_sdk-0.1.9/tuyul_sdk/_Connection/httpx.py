import ssl
import chardet
import httpx as _httpx
from typing import Dict, Optional
from httpx import Client

from .utils import SSLContext, MY_CHIPER, certificate, ProxyParams
from ..Utils import version

class httpx:

    @staticmethod
    def __autodetect__(content):
        return chardet.detect(content).get('encoding')
    
    def __new__(cls, timeout: int = 15, extra_headers: Dict[str, str] = dict(), proxyParams: Optional[ProxyParams] = None) -> Client:
        if not proxyParams: proxy_url = None
        else: proxy_url = proxyParams.URL
        context = SSLContext()
        context.set_ciphers(MY_CHIPER)
        context.options &= ~ssl.OP_NO_TICKET  # pylint: disable=E1101
        context.load_verify_locations(cafile=certificate())
        timeouts    = _httpx.Timeout(float(timeout), connect=60.0)
        transport   = _httpx.HTTPTransport(http2=True, retries=3.0)
        header: Dict[str, str] = dict()
        try:
            for k, v in zip(extra_headers.keys(), extra_headers.values()): header.update(**{k.lower():v})
            if not header.get('User-Agent'.lower()):
                header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        except AttributeError:
            if not header.get('User-Agent'.lower()):
                header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        return _httpx.Client(http2=True, cert=context, verify=context, proxies=proxy_url, headers=header, default_encoding=cls.__autodetect__, timeout=timeouts, transport=transport)
