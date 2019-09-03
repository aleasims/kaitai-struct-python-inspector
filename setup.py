import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kspyspector',
    version='0.1.0',
    description='Tree builder for Kaitai Struct parsed objects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aleasims/kaitai-struct-python-inspector',
    author='Evgin Alexander',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
    keywords='kaitaistruct parsetree',
    packages=['kspyspector'],
    package_dir={'kspyspector': 'kspyspector'},
    python_requires='>=3.5',
    install_requires=[
        'kaitaistruct>=0.8',
        'graphviz>=0.11.1',
        'pyyaml>=5.1.1'
    ],
    package_data={
        'kspyspector': ['tests/data/*'],
    },
    entry_points={
        'console_scripts': [
            'kspyspector=kspyspector.cli:main',
        ]
    }
)
