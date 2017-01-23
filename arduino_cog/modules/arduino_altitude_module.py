from up.modules.base_altitude_provider import BaseAltitudeProvider

from arduino_cog.modules.arduino_module import ArduinoModule


class ArduinoAltitudeModule(BaseAltitudeProvider):
    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__altitude = 0
        self.__arduino_module = None

    def _execute_start(self):
        self.__arduino_module = self.up.get_module(ArduinoModule.__name__)
        if self.arduino_module is None:
            self.logger.critical("Arduino Module not found")
            raise ValueError("Arduino Module not found")
        return self.__arduino_module.started

    def _on_altitude_changed(self, new_altitude):
        super()._on_altitude_changed(new_altitude)
        self.arduino_module.send_altitude(new_altitude)

    @property
    def arduino_module(self):
        return self.__arduino_module
