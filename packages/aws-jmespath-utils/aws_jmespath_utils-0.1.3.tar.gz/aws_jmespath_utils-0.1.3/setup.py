# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_jmespath_utils']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'aws-jmespath-utils',
    'version': '0.1.3',
    'description': 'jmespath custom functions for filtering AWS resources by tag2',
    'long_description': '# aws-jmespath-utils',
    'author': 'Oguzhan Yilmaz',
    'author_email': 'oguzhanylmz271@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
