from up.registrar import UpRegistrar


class Registrar(UpRegistrar):
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
        return True
