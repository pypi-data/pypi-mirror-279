import os
from setuptools import setup

import nrt_string_utils

PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(os.path.join(PATH, 'README.md')) as f:
    readme = f.read()

setup(
    name='nrt-string-utils',
    version=nrt_string_utils.__version__,
    author='Eyal Tuzon',
    author_email='eyal.tuzon.dev@gmail.com',
    description='String utilities in Python',
    keywords='python python3 python-3 utilities utils util tool tools'
             ' nrt nrt-utils string string-utils string-utilities nrt-string-utils'
             ' nrt-string-utilities',
    long_description_content_type='text/markdown',
    long_description=readme,
    url='https://github.com/etuzon/python-nrt-string-utils',
    packages=['nrt_utils'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[requirements],
    data_files=[('', ['requirements.txt'])],
)
