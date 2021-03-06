from up.modules.up_location_provider import UpLocationProvider

from arduino_cog.modules.arduino_module import ArduinoModule


class ArduinoLocationModule(UpLocationProvider):
    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__arduino_module = None

    def _execute_start(self):
        super()._execute_start()
        self.__arduino_module = self.up.get_module(ArduinoModule)
        if self.arduino_module is None:
            self.logger.critical("Arduino Module not found")
            raise ValueError("Arduino Module not found")
        return self.__arduino_module.started

    def _on_location_changed(self):
        super()._on_location_changed()
        if self.started:
            self.arduino_module.send_location(self.latitude, self.longitude)

    def load(self):
        return True

    @property
    def arduino_module(self) -> ArduinoModule:
        return self.__arduino_module
