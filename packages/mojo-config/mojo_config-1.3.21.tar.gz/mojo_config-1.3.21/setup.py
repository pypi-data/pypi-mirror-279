# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.config', 'mojo.config.sources', 'mojo.config.synchronization']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=41.0.3,<43.0.0',
 'mojo-collections>=1.3.16,<1.4.0',
 'mojo-credentials>=1.3.17,<1.4.0',
 'mojo-errors>=1.3.9,<1.4.0',
 'mojo-extension>=1.3.19,<1.4.0',
 'mojo-startup>=1.3.11,<1.4.0',
 'pyyaml>=6.0.1,<7.0.0',
 'requests>=2.32.3,<3.0.0']

extras_require = \
{'couchdb': ['couchdb>=1.2,<2.0'], 'mongodb': ['pymongo[srv]>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'mojo-config',
    'version': '1.3.21',
    'description': 'Automation Mojo Configuration Package',
    'long_description': "=====================================\nAutomation Mojo Configuration Package\n=====================================\nThe Automation Mojo configuration package is a package that provides configuration management for distributed\nautomation projects.\n\n=================\nCode Organization\n=================\n* .vscode - Common tasks\n* development - This is where the runtime environment scripts are located\n* repository-setup - Scripts for homing your repository and to your checkout and machine setup\n* userguide - Where you put your user guide\n* source/packages - Put your root folder here 'source/packages/(root-module-folder)'\n* source/sphinx - This is the Sphinx documentation folder\n* workspaces - This is where you add VSCode workspaces templates and where workspaces show up when homed.\n\n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`\n- `Coding Standards <userguide/10-00-coding-standards.rst>`\n",
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
