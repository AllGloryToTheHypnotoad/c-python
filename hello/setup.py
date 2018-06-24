#!/usr/bin/env python

from setuptools import setup, Extension, Command
# from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution
from colorama import Fore, Back, Style
from shutil import rmtree

# from setuptools.command.test import test as TestCommand

import os

# Load the package's __version__.py module as a dictionary.
# about = {}
# if not VERSION:
#     with open(os.path.join(here, NAME, '__version__.py')) as f:
#         exec(f.read(), about)
# else:
#     about['__version__'] = VERSION

class BuildCommand2(Command):
    """Build binaries/packages"""
    pkg = None
    test = True     # run tests
    py2 = True      # build python 2 package
    py3 = True      # build python 3 package
    rm_egg = False  # rm egg-info directory
    rm_so = False   # rm shared library, this is for c extensions

    description = 'Build and publish the package.'

    # # The format is (long option, short option, description)
    user_options = []

    def initialize_options(self):
        # Each user option must be listed here with their default value.
        pass

    def finalize_options(self):
        pass

    def cprint(self, color, msg):
        print(color + msg + Style.RESET_ALL)

    def rmdir(self, folder):
        try:
            rmtree(folder)
            self.cprint(Fore.RED, ">> Deleted Folder {}".format(folder))
        except OSError:
            pass

    def rm(self, file):
        try:
            os.system('rm {}'.format(file))
            self.cprint(Fore.RED, ">> Deleted File {}".format(file))
        except OSError:
            pass

    def run(self):
        if not self.pkg:
            raise Exception('BuildCommand::pkg is not set')

        print(Fore.BLUE + '+----------------------------------')
        print('| Package: {}'.format(self.pkg))
        print('+----------------------------------')
        print('| Python 2: tests & build: {}'.format(self.py2))
        print('| Python 3: tests & build: {}'.format(self.py3))
        print('+----------------------------------\n\n' + Style.RESET_ALL)

        pkg = self.pkg
        print('Delete dist directory and clean up binary files')

        self.rmdir('dist')
        self.rmdir('build')
        self.rmdir('.eggs')
        if self.rm_egg:
            self.rmdir('{}.egg-info'.format(pkg))
        if self.rm_so:
            self.rm('*.so')
            self.rm('{}/*.so'.format(pkg))
        self.rm('{}/*.pyc'.format(pkg))
        self.rmdir('{}/__pycache__'.format(pkg))

        if self.test:
            print('Run Nose tests')
            if self.py2:
                ret = os.system("unset PYTHONPATH; python2 -m nose -w tests -v test.py")
                if ret > 0:
                    print('<<< Python2 nose tests failed >>>')
                    return
            if self.py3:
                ret = os.system("unset PYTHONPATH; python3 -m nose -w tests -v test.py")
                if ret > 0:
                    print('<<< Python3 nose tests failed >>>')
                    return

        print('Building packages ...')
        self.cprint(Fore.WHITE + Back.GREEN,'>> Python source ----------------------------------------------')
        os.system("unset PYTHONPATH; python setup.py sdist")
        if self.py2:
            self.cprint(Fore.GREEN,'>> Python 2 ---------------------------------------------------')
            os.system("unset PYTHONPATH; python2 setup.py bdist_wheel")
        if self.py3:
            self.cprint(Fore.BLUE,'>> Python 3 ---------------------------------------------------')
            os.system("unset PYTHONPATH; python3 setup.py bdist_wheel")


clib = Extension(
    "helloworld",
    ["c/libmypy.c", "c/add.c"]
)


PACKAGE_NAME = 'hello'
VERSION = "0.0.2"
BuildCommand2.pkg = PACKAGE_NAME
BuildCommand2.test = False
# BuildCommand2.rm_egg = True
BuildCommand2.rm_so = True
PublishCommand.pkg = PACKAGE_NAME
PublishCommand.version = VERSION

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=[PACKAGE_NAME],
    ext_modules=[clib],
    cmdclass={
        'publish': PublishCommand,
        'make': BuildCommand2,
        # 'clean': CleanCommand
    }
)
