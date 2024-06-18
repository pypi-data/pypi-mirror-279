# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.startup']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.11.0,<5.0.0']

setup_kwargs = {
    'name': 'mojo-startup',
    'version': '1.3.11',
    'description': 'Automation Mojo Startup Package',
    'long_description': '=======================\nmojo-startup\n=======================\nThis package sets up a pattern for extremely early pre-configuration of variable extensibility\nhook for the startup configuration.  This module looks for a single environment variable to be set:\n\n.. code::\n\n    MJR_STARTUP_SETTINGS\n\nThe value of this variable is accessed like so:\n\n.. code::\n\n    from mojo.startup.startupvariables import MOJO_STARTUP_VARIABLES\n    \n    print(MOJO_STARTUP_VARIABLES.MJR_STARTUP_SETTINGS)\n\n\nThe `MJR_STARTUP_SETTINGS` is an environment variable that is is set to the path for a config file that should point to the\nconfiguration file that is used to startup the environment of a process.\n\nThe default value for the `MJR_STARTUP_SETTINGS` variable is `~/.mojo.config`.\n\nThe `mojo-startup` module makes a singleton `ConfigParser` available for other modules to use.  This\nconfiguration parser can be accessed by:\n\n.. code::\n    \n    from mojo.startup.wellknown import StartupConfigSingleton\n    \n    cparser = StartupConfigSingleton()\n    \n    defaults_section = cparser["DEFAULTS"]\n    someval = defaults_section["SOME_VARIABLE"]\n\n===========\nDescription\n===========\nThis module does one very important thing.  It establishes the path for all other \'mojo\' packages\non where to load default config from.  This is very important because it provides extensibility\nas early as possible before the running of any code.\n\nThe pattern established for defaults for variables is:\n* Variable is set to a hard coded default\n* Startup configuration is checked for an override\n* The environment variables are checked for an override\n\n=================\nCode Organization\n=================\n* .vscode - Common tasks\n* development - This is where the runtime environment scripts are located\n* repository-setup - Scripts for homing your repository and to your checkout and machine setup\n* userguide - Where you put your user guide\n* source/packages - Put your root folder here \'source/packages/(root-module-folder)\'\n* source/sphinx - This is the Sphinx documentation folder\n* workspaces - This is where you add VSCode workspaces templates and where workspaces show up when homed.\n\n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`\n- `Coding Standards <userguide/10-00-coding-standards.rst>`\n',
    'author': 'Myron W. Walker',
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
