from setuptools import setup

setup(
    name='arduino_cog',
    version='0.1.3',
    packages=['arduino_cog', 'arduino_cog.modules', 'arduino_cog.commands'],
    url='https://github.com/Rashitko/arduino_cog',
    download_url='https://github.com/Rashitko/arduino_cog/master/tarball/',
    license='MIT',
    author='Michal Raska',
    author_email='michal.raska@gmail.com',
    description='',
    install_requires=['up', 'pyyaml', 'serial_cog>=0.1.4'],
    package_data={
        'arduino_cog': ['arduino_cog/registered_modules.yml']
    }

)
