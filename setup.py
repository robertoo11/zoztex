print('D4rk3st says HII')

print('Installing required packages, hold on ..')

from setuptools import setup

packages = [
    "zoztex",
    "zoztex.exceptions",
    "zoztex.http",
    "zoztex.utils",
    "zoztex.ws",
    "zoztex.ws.channels",
    "zoztex.ws.objects",
]

package_data = {"": ["*"]}

install_requires = [
    "beautifulsoup4==4.11.2",
    "certifi==2022.12.7",
    "greenlet>=2.0.1",
    "playwright>=1.39.0",
    "pyOpenSSL>=23.1.1",
    "pytz>=2023.3",
    "requests-toolbelt>=1.0.0",
    "requests>=2.31.0",
    "urllib3>=2.0.5",
    "websocket-client==1.6.3",
    "websockets==11.0.3",
]

setup_kwargs = {
    "name": "ZozTex",
    "version": "1.0.0",
    "description": "📈 ZozTex is an Auto-trading bot built by D4rk3st. ",
    "long_description": '<div align="center">\n<img src="https://static.scarf.sh/a.png?x-pxid=cf317fe7-2188-4721-bc01-124bb5d5dbb2" />\n\n## <img src="https://github.com/SantiiRepair/quotexpy/blob/main/.github/images/quotex-logo.png?raw=true" height="56"/>\n\n\n**📈 QuotexPy is a library to easily interact with qxbroker.**\n\n______________________________________________________________________\n\n[![License](https://img.shields.io/badge/License-LGPL--2.1-magenta.svg)](https://www.gnu.org/licenses/gpl-3.0.txt)\n[![PyPI version](https://badge.fury.io/py/quotexpy.svg)](https://badge.fury.io/py/quotexpy)\n![GithubActions](https://github.com/SantiiRepair/quotexpy/actions/workflows/pylint.yml/badge.svg)\n\n</div>\n\n______________________________________________________________________\n\n## Installing\n\n📈 QuotexPy is tested on Ubuntu 18.04 and Windows 10 with **Python >= 3.10, <= 3.12.**\n```bash\npip install quotexpy\n```\n\nIf you plan to code and make changes, clone and install it locally.\n\n```bash\ngit clone https://github.com/SantiiRepair/quotexpy.git\npip install -e .\n```\n\n## Import\n```python\nfrom quotexpy import Quotex\n```\n\n## Examples\nFor examples check out [some](https://github.com/SantiiRepair/quotexpy/blob/main/example/main.py) found in the `example` directory.\n\n## Donations\nIf you feel like showing your love and/or appreciation for this project, then how about shouting us a coffee ;)\n\n[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/SantiiRepair)\n\n## Acknowledgements\n- Thanks to [@cleitonleonel](https://github.com/cleitonleonel) for the initial base implementation of the project 🔥\n- Thanks to [@ricardospinoza](https://github.com/ricardospinoza) for solving the `trade` error in the code 🚀\n\n## Notice \nThis project is a clone of the [original](https://github.com/cleitonleonel/pyquotex) project, because the original project was discontinued, I updated it with the help of [collaborators](https://github.com/SantiiRepair/quotexpy/graphs/contributors) in the community so that it is accessible to everyone.\n',
    
    "maintainer": "None",
    "maintainer_email": "None",
    "url": "hackerzz.com",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.10,<3.13",
}


setup(**setup_kwargs)