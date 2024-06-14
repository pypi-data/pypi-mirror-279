# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuyul_sdk',
 'tuyul_sdk.Utils',
 'tuyul_sdk.Utils._base',
 'tuyul_sdk._Cipher',
 'tuyul_sdk._Connection',
 'tuyul_sdk._Connection._async',
 'tuyul_sdk._Connection._certificate',
 'tuyul_sdk._Gmail']

package_data = \
{'': ['*']}

install_requires = \
['base58==2.1.1',
 'bs4>=0.0.2,<0.0.3',
 'chardet==5.2.0',
 'colorama==0.4.6',
 'google-api-python-client==2.131.0',
 'httpx[http2,socks]==0.27.0',
 'lxml==5.2.2',
 'pycryptodomex==3.20.0',
 'python-dotenv>=1.0.1,<2.0.0',
 'random-user-agent==1.0.1',
 'requests-toolbelt==0.10.1',
 'requests==2.31.0',
 'sqlalchemy-utils==0.41.2',
 'sqlalchemy==2.0.30',
 'urllib3==1.26.15',
 'useragenter==1.3.1']

setup_kwargs = {
    'name': 'tuyul-sdk',
    'version': '0.1.9',
    'description': '',
    'long_description': '',
    'author': 'DesKaOne',
    'author_email': 'DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
