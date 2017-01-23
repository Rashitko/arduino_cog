from up.modules.base_location_provider import BaseLocationProvider

from arduino_cog.modules.arduino_module import ArduinoModule


class ArduinoLocationModule(BaseLocationProvider):
    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__arduino_module = None

    def _execute_start(self):
        self.__arduino_module = self.up.get_module(ArduinoModule.__name__)
        if self.arduino_module is None:
            self.logger.critical("Arduino Module not found")
            raise ValueError("Arduino Module not found")
        return self.__arduino_module.started

    def _on_location_changed(self, lat, lon):
        super()._on_location_changed(lat, lon)
        self.arduino_module.send_location(lat, lon)

    @property
    def arduino_module(self) -> ArduinoModule:
        return self.__arduino_module

