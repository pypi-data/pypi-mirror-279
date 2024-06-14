# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydgram']

package_data = \
{'': ['*']}

install_requires = \
['master-tuyul-sdk>=0.1.2,<0.2.0', 'pyrogram>=2.0.106,<3.0.0']

setup_kwargs = {
    'name': 'pydgram',
    'version': '0.0.1rc10',
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
