# setup.py

from setuptools import setup, find_packages

setup(
    name='beholdr_io_sdk',
    version='0.1.0',
    description='A Python SDK for interacting with Beholdr.io\'s Metrics API.',
    author='Beholdr.io',
    author_email='devin@beholdr.io',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
