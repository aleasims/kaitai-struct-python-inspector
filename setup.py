import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
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
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='kaitaistruct parsetree',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5',
    install_requires=['peppercorn'],  # Optional
    package_data={
        'sample': ['package_data.dat'],
    },
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    }
)