# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.runtime']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=7.0.4,<8.0.0',
 'mojo-collections>=1.3.16,<1.4.0',
 'mojo-config>=1.3.21,<1.4.0',
 'mojo-errors>=1.3.9,<1.4.0',
 'mojo-extension>=1.3.19,<1.4.0',
 'mojo-xmodules>=1.3.23,<1.4.0']

setup_kwargs = {
    'name': 'mojo-runtime',
    'version': '1.3.30',
    'description': 'Automation Mojo Runtime Module (mojo-runtime)',
    'long_description': '# Automation Mojo Runtime\nThe Automation Mojo - Runtime package is used to create various types of runtime environments\nsuch as Test Run, Console Command, Interactive Console and Service.  The package helps provide\nthe functionality and expected behaviors for path management and logging for each of these\ntypes of application environments.\n',
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
