import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="Underscore",
    version="0.0.4",
    packages=["underscore"],
    author="Huan Do",
    author_email="doboy0@gmail.com",
    description=("Obfuscating code by changing"
                 " the variable names to underscores"),
    long_description=read("README.md"),
    url="https://github.com/Doboy/Dunderscore",
    install_requires=["also"],
    tests_require=["nose", "nose-cov"],
    scripts=["scripts/_"],
    )
