# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo',
 'mojo.landscaping',
 'mojo.landscaping.agents',
 'mojo.landscaping.client',
 'mojo.landscaping.cluster',
 'mojo.landscaping.coordinators',
 'mojo.landscaping.coupling',
 'mojo.landscaping.layers',
 'mojo.landscaping.service']

package_data = \
{'': ['*']}

install_requires = \
['mojo-config>=1.3.21,<1.4.0',
 'mojo-credentials>=1.3.17,<1.4.0',
 'mojo-extension>=1.3.19,<1.4.0',
 'mojo-interfaces>=1.3.5,<1.4.0',
 'mojo-xmodules>=1.3.23,<1.4.0']

setup_kwargs = {
    'name': 'mojo-landscaping',
    'version': '1.3.7',
    'description': 'Automation Mojo Landscaping Package',
    'long_description': '=======================\npython-package-template\n=======================\nThis is a template repository that can be used to quickly create a python package project.\n\n=========================\nFeatures of this Template\n=========================\n* Machine Setup\n* Virtual Environment Setup (Poetry)\n* PyPi Publishing\n* Sphinx Documentation\n\n========================\nHow to Use This Template\n========================\n- Click the \'Use this template\' button\n- Fill in the information to create your repository\n- Checkout your new repository\n- Change the following in \'repository-config.ini\'\n\n  #. \'PROJECT NAME\'\n  #. \'REPOSITORY_NAME\'\n\n- If you have machine dependencies to add, put them in \'setup-ubuntu-machine\'\n- Modify the pyproject.toml file with the correct package-name, author, publishing information, etc.\n- Rename the VSCODE workspace file \'mv workspaces/default-workspace.template workspaces/(project name).template\'\n- Replace the README.rst file with your own README\n- Update the LICENSE.txt file with your copyright information and license.\n- Add your dependencies with python poetry \'poetry add (dependency name)\'\n- Drop your package code in \'source/packages\'\n- Modify the name of your package root in \'pyproject.toml\'\n\n  #. \'packages = [{include="(root folder name)", from="source/packages"}]\'\n\n=================\nCode Organization\n=================\n* .vscode - Common tasks\n* development - This is where the runtime environment scripts are located\n* repository-setup - Scripts for homing your repository and to your checkout and machine setup\n* userguide - Where you put your user guide\n* source/packages - Put your root folder here \'source/packages/(root-module-folder)\'\n* source/sphinx - This is the Sphinx documentation folder\n* workspaces - This is where you add VSCode workspaces templates and where workspaces show up when homed.\n\n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`\n- `Coding Standards <userguide/10-00-coding-standards.rst>`\n',
    'author': 'Myron W Walker',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
