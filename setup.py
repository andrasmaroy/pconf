from os import path
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


setup(
    name="pconf",
    version="1.10.0",
    author="Andras Maroy",
    author_email="andras@maroy.hu",
    description=("Hierarchical python configuration with files, environment variables, command-line arguments."),
    license="MIT",
    keywords="configuration hierarchical",
    url="https://github.com/andrasmaroy/pconf",
    packages=['pconf', 'pconf.store'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    install_requires=['pyyaml', 'deepmerge'],
    extras_require={
        'test': ['pytest', 'mock'],
    },
)
