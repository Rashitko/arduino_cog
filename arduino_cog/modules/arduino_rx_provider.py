from up.providers.base_rx_provider import BaseRXProvider

from arduino_cog.modules.arduino_module import ArduinoModule


class ArduinoRXProvider(BaseRXProvider):
    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__arduino_module = None
        self.__channels = {'ailerons': 1500, 'elevator': 1500, 'throttle': 1000, 'rudder': 1500}

    def _execute_initialization(self):
        super()._execute_initialization()

    def _execute_start(self):
        self.__arduino_module = self.up.get_module(ArduinoModule)
        if self.__arduino_module is None:
            self.logger.critical("Arduino Module not found")
            raise ValueError("Arduino Module not found")
        return self.__arduino_module.started

    def _execute_stop(self):
        super()._execute_stop()

    def get_channels(self):
        return self.__channels

    def load(self):
        return True
