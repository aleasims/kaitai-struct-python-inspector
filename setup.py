"""
    Development installation:
pip install -e .[dev]

    Normal installation
pip install .
"""

import os

from setuptools import setup

import kspyspector

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requierments = [
    'kaitaistruct>=0.8',
    'graphviz>=0.11.1',
    'pyyaml>=5.1.1'
]

requierments_dev = [
    'pylint',
    'flake8',
    'autopep8'
]

data_paths = {'kspyspector': ['tests/data/*']}
entry_points = {'console_scripts': ['kspyspector=scripts.main:main']}

classifiers = '''
Development Status :: 3 - Alpha
Programming Language :: Python :: 3
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
'''.rstrip().lstrip().split('\n')


setup(
    name='kspyspector',
    version=kspyspector.__version__,
    description='Tree builder for Kaitai Struct parsed objects',
    long_description=long_description,
    url='https://github.com/aleasims/kaitai-struct-python-inspector',
    author=kspyspector.__author__,
    classifiers=classifiers,
    keywords='kaitaistruct parsetree',
    packages=['kspyspector'],
    package_dir={'kspyspector': 'kspyspector'},
    python_requires='>=3.5',
    install_requires=requierments,
    extras_require={'dev': requierments_dev},
    package_data=data_paths,
    entry_points=entry_points
)
