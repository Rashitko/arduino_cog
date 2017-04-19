import serial_cog.registrar
from up.registrar import UpRegistrar


class Registrar(UpRegistrar):
    CONFIG_FILE_NAME = 'arduino.yml'
    PORT_KEY = 'port'
    BAUD_RATE_KEY = 'baud_rate'

    CONFIG_TEMPLATE = """\
port: # Place your port here
baud_rate: 9600
"""
    PIDS_CONFIG_FILE_NAME = 'pids.yml'
    PIDS_CONFIG_TEMPLATE = """\
rate:
  ailerons:
    p: 6
    i: 0
    d: 0
  elevator:
    p: 6
    i: 0
    d: 0
stabilize:
  ailerons:
    p: 0.7
    i: 0
    d: 0
  elevator:
    p: 0.7
    i: 0
    d: 0
    """

    def __init__(self):
        super().__init__('arduino_cog')

    def register(self):
        external_modules = self._load_external_modules()
        if external_modules is not None:
            self._register_modules_from_file()
            self._create_config(self.CONFIG_FILE_NAME, self.CONFIG_TEMPLATE)
            self._create_config(self.PIDS_CONFIG_FILE_NAME, self.PIDS_CONFIG_TEMPLATE)
            self._print_info('Registering serial_cog:')
            return serial_cog.registrar.Registrar().register()
        return False
