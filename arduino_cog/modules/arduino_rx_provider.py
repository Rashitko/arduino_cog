from up.providers.base_rx_provider import BaseRXProvider

from arduino_cog.modules.arduino_module import ArduinoModule


class ArduinoRXProvider(BaseRXProvider):
    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    RUD_KEY = 'rudder'
    THR_KEY = 'throttle'
    ELE_KEY = 'elevator'
    AIL_KEY = 'ailerons'

    def __init__(self):
        super().__init__()
        self.__arduino_module = None
        self.__channels = {self.AIL_KEY: 1500, self.ELE_KEY: 1500, self.THR_KEY: 1000, self.RUD_KEY: 1500}

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

    def set_channels(self, values):
        self.__channels = values

    def create_channels_values(self, ail, ele, thr, rud):
        return {self.AIL_KEY: ail, self.ELE_KEY: ele, self.THR_KEY: thr, self.RUD_KEY: rud}

    def load(self):
        return True
