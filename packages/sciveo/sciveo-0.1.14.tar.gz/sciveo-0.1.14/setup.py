#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2023
#

from setuptools import setup, find_packages
from sciveo.version import __version__

setup(
    name='sciveo',
    version=__version__,
    packages=find_packages(),
    install_requires=[
      'numpy>=0.0.0',
      'requests>=0.0.0',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    extras_require={
      'mon': [
        'psutil>=0.0.0',
      ],
      'net': [
        'netifaces>=0.0.0',
      ],
      'all': [
        'psutil>=0.0.0',
        'netifaces>=0.0.0',
      ]
    },
    py_modules=['sciveo'],
    entry_points={
      'console_scripts': [
        'sciveo=sciveo.cli:main',
      ],
    },
)
