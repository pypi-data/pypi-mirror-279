import os
from setuptools import setup

import nrt_math_utils

PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(os.path.join(PATH, 'README.md')) as f:
    readme = f.read()

setup(
    name='nrt-math-utils',
    version=nrt_math_utils.__version__,
    author='Eyal Tuzon',
    author_email='eyal.tuzon.dev@gmail.com',
    description='Math utilities in Python',
    keywords='python python3 python-3 tool tools math mathematics utilities utils util'
             ' nrt nrt-utils nrt-utilities math-utils math-utilities'
             ' nrt-utilities nrt-math-utils nrt-math-utilities',
    long_description_content_type='text/markdown',
    long_description=readme,
    url='https://github.com/etuzon/python-nrt-math-utils',
    packages=['nrt_math_utils'],
    classifiers=[
        'Programming Language :: Python :: 3',
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
