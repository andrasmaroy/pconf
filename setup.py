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
    version="0.3.0",
    author="Andras Maroy",
    author_email="andras@maroy.hu",
    description=("Hierarchical python configuration with files, environment variables, command-line arguments."),
    license="MIT",
    keywords="configuration hierarchical",
    url="https://github.com/andrasmaroy/pconf",
    packages=['pconf', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    extras_require={
        'test': ['pytest', 'mock'],
    },
)
