try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# http://stackoverflow.com/a/22147112
import os
if os.environ.get('USER','') == 'vagrant':
    del os.link

with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

with open('README.rst') as f:
    readme = f.read()

config = {
    'name': 'betfairng',
    'packages': ['betfairng'],
    'version': version,
    'description': 'Client library for Betfair API Next-Generation',
    'long_description': readme,
    'author': 'Russell Gray',
    'author_email': 'russgray@gmail.com',
    'url': 'http://www.tagwager.com/',
    'download_url': 'http://www.tagwager.com/',
    'keywords': ['betfair', 'aping', 'tagwager'],
    'install_requires': ['requests'],
    'license': 'BSD 2-Clause',
    'classifiers': [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
}

setup(**config)
