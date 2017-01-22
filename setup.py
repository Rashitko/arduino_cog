import os

import yaml
from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        upm_install_path = os.environ.get('UPM_INSTALL_PATH', os.getcwd())
        path = os.path.join(upm_install_path, 'external_modules.yml')
        with open(path) as external_mods_file:
            external_mods = yaml.load(external_mods_file)
            if external_mods is None:
                external_mods = {}
        with open(path, 'w+') as external_mods_file:
            external_mods['arduino_cog'] = {
                'modules': [
                    {'prefix': 'arduino_cog.modules.arduino_module', 'class_name': 'ArduinoModule'},
                    {'prefix': 'arduino_cog.modules.arduino_altitude_module', 'class_name': 'ArduinoAltitudeModule'},
                    {'prefix': 'arduino_cog.modules.arduino_heading_module', 'class_name': 'ArduinoHeadingModule'},
                    {'prefix': 'arduino_cog.modules.arduino_location_module', 'class_name': 'ArduinoLocationModule'}
                ],
                'recorders': []
            }
            yaml.dump(external_mods, external_mods_file)
        install.run(self)


setup(
    name='arduino_cog',
    version='0.1',
    packages=['arduino_cog', 'arduino_cog.modules'],
    url='',
    license='',
    author='Michal Raska',
    author_email='michal.raska@gmail.com',
    description='',
    install_requires=['up', 'serial_cog', 'pyyaml'],
    dependecy_links=[
        'git+https://github.com/Rashitko/serial_provider_cog/tarball/master#egg=serial_cog'
    ],
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostInstallCommand,
    }
)
