# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['podping_schemas',
 'podping_schemas.org',
 'podping_schemas.org.podcastindex',
 'podping_schemas.org.podcastindex.podping',
 'podping_schemas.org.podcastindex.podping.hivewriter']

package_data = \
{'': ['*']}

install_requires = \
['capnpy>=0.10.0,<0.11.0', 'python-jsonschema-objects>=0.5.4,<0.6.0']

setup_kwargs = {
    'name': 'podping-schemas',
    'version': '1.0.1',
    'description': '',
    'long_description': '# podping-schemas-python\n\nPython schema files for Podping',
    'author': 'Alecks Gates',
    'author_email': 'agates@mail.agates.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
