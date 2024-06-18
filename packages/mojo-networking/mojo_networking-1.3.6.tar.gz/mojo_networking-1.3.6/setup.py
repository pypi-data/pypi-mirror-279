# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.networking']

package_data = \
{'': ['*']}

install_requires = \
['netifaces>=0.11.0,<0.12.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'mojo-networking',
    'version': '1.3.6',
    'description': 'Automation Mojo Netorking Package (mojo-networking)',
    'long_description': '# python-package-template\nThis is a template repository that can be used to quickly create a python package project.\n',
    'author': 'Myron Walker',
    'author_email': 'myron.walker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://automationmojo.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
