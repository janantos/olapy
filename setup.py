# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import zipfile
from os.path import expanduser
from shutil import copyfile

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import find_packages, setup

RUNNING_TOX = 'RUNNING_TOX' in os.environ

# from setuptools.command.install import install


# class PostDevelopCommand(develop):
#     """Post-installation for development mode."""
#     def run(self):
#         # PUT YOUR PRE-INSTALL SCRIPT HERE or CALL A FUNCTION
#         print('111111111111111111111111')
#         develop.run(self)
#
#         basedir = expanduser('~')
#         if not os.path.isfile(os.path.join(basedir, 'olapy-data', 'olapy.db')):
#             # try:
#             from manage import initdb
#             initdb()
#         # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
#
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         # PUT YOUR PRE-INSTALL SCRIPT HERE or CALL A FUNCTION
#
#         install.run(self)
#         # initiate cubes examples
#         if RUNNING_TOX:
#             home_directory = os.environ.get('HOME_DIR')
#         else:
#             home_directory = expanduser("~")
#
#         if not os.path.isdir(os.path.join(home_directory, 'olapy-data', 'cubes')):
#             try:
#                 os.makedirs(os.path.join(home_directory, 'olapy-data', 'cubes'))
#                 zip_ref = zipfile.ZipFile('cubes_templates/cubes_temp.zip', 'r')
#                 zip_ref.extractall(os.path.join(home_directory, 'olapy-data', 'cubes'))
#                 zip_ref.close()
#             except:
#                 raise Exception('unable to create cubes directory !')


session = PipSession()
_install_requires = parse_requirements('requirements.txt', session=session)
install_requires = [str(ir.req) for ir in _install_requires]

setup(
    name='olapy',
    version="0.3.1",
    packages=find_packages(),
    author="Abilian SAS",
    author_email="contact@abilian.com",
    description="OLAP Engine",
    url='https://github.com/abilian/olapy',
    # TODO fix tox problem with path
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    include_package_data=False,
    # cmdclass={
    #     # 'develop': PostDevelopCommand,
    #     'install': PostInstallCommand,
    # },
    classifiers=[
        "Programming Language :: Python",
        'Development Status :: 3 - Alpha',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        # "Topic :: Business intelligence",
    ],)

# # generate and set secret key
# os.environ["SECRET_KEY"]

if RUNNING_TOX:
    home_directory = os.environ.get('HOME_DIR')
else:
    home_directory = expanduser("~")

if not os.path.isdir(os.path.join(home_directory, 'olapy-data', 'cubes')):
    os.makedirs(os.path.join(home_directory, 'olapy-data', 'cubes'))
    zip_ref = zipfile.ZipFile('cubes_templates/cubes_temp.zip', 'r')
    zip_ref.extractall(os.path.join(home_directory, 'olapy-data', 'cubes'))
    zip_ref.close()

if not os.path.isfile(os.path.join(home_directory, 'olapy-data','olapy-config.xml')):
    copyfile('config/olapy-config.xml', os.path.join(home_directory, 'olapy-data','olapy-config.xml'))


