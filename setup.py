import os
import shutil
from setuptools import setup
from distutils.command import install as install_module

class Install(install_module.install):
    def run(self):
        self._copyFiles()
        install_module.install.run(self)

    def _copyFiles(self):
        if os.path.isfile('underscore') or os.path.isdir('underscore'):
            shutil.rmtree('underscore')
        shutil.copytree('src', 'underscore')
        # from underscore import _
        # _('src', 'underscore', verbose=True)

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
    scripts=["bin/_"],
    cmdclass = {
        'install' : Install,
        },
    )
