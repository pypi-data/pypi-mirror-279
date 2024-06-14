from typing import Dict
import aiohttp
from aiohttp_proxy import ProxyConnector

from ...Utils import Report, Proxy, logger, version as VERSION_SDK

class AsyncConnection(Report):

    @staticmethod
    def check_headers(extra_headers: Dict[str, str]):
        header: Dict[str, str] = dict()
        if len(extra_headers) > 0:
            for k, v in zip(extra_headers.keys(), extra_headers.values()):
                header.update(**{k.lower() : v})
        if not header.get('User-Agent'.lower()):
            header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(VERSION_SDK)})
        return header
    
    @classmethod
    async def check_proxy(cls, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info('{}, Proxy IP: {}'.format('AsyncConnection', ip))
        except Exception as error:
            logger.error('{}, Proxy: {}, Error: {}'.format('AsyncConnection', proxy, error))
    
    async def __new__(cls, extra_headers: dict, proxy: str = None) -> aiohttp.ClientSession:
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None
        while True:
            http_client = aiohttp.ClientSession(headers=cls.check_headers(extra_headers), connector=proxy_conn)
            if proxy:
                await cls.check_proxy(http_client=http_client, proxy=proxy)
            if not http_client.closed:
                logger.info('{}, is Connected'.format('AsyncConnection'))
                return http_client
            else:
                logger.error('{}, not Connected'.format('AsyncConnection'))
