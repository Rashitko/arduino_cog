from up.registrar import UpRegistrar
import serial_cog.registrar



class Registrar(UpRegistrar):
    CONFIG_FILE_NAME = 'arduino.yml'
    PORT_KEY = 'port'
    BAUD_RATE_KEY = 'baud_rate'

    CONFIG_TEMPLATE = """\
port: # Place your port here
baud_rate: 9600
"""

    def __init__(self):
        super().__init__('arduino_cog')

    def register(self):
        external_modules = self._load_external_modules()
        if external_modules is not None:
            self._register_module('ArduinoModule', 'arduino_cog.modules.arduino_module')
            self._register_module('ArduinoAltitudeModule', 'arduino_cog.modules.arduino_altitude_module')
            self._register_module('ArduinoHeadingModule', 'arduino_cog.modules.arduino_heading_module')
            self._register_module('ArduinoLocationModule', 'arduino_cog.modules.arduino_location_module')
            self._write_external_modules()
        self._create_config(self.CONFIG_FILE_NAME, self.CONFIG_TEMPLATE)
        self._print_info('Registering serial_cog:')
        return serial_cog.registrar.Registrar().register()
