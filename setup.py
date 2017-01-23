import os

import yaml
from setuptools import setup
from setuptools.command.install import install

setup(
    name='arduino_cog',
    version='0.1.2',
    packages=['arduino_cog', 'arduino_cog.modules'],
    url='https://github.com/Rashitko/arduino_cog',
    download_url='https://github.com/Rashitko/arduino_cog/master/tarball/',
    license='MIT',
    author='Michal Raska',
    author_email='michal.raska@gmail.com',
    description='',
    install_requires=['up', 'pyyaml', 'serial_cog'],
)
