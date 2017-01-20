from serial_provider.modules.serial_module import SerialProvider
from up.base_started_module import BaseStartedModule


class ArduinoModule(BaseStartedModule):
    def __init__(self):
        super().__init__()
        self.__serial_module = None

    def _execute_initialization(self):
        pass

    def _execute_start(self):
        self.__serial_module = self.up.get_module(SerialProvider)
        if self.__serial_module is None:
            self.logger.critical('SerialProvider not available')
            raise ValueError('SerialProvider not available')
        return True

    def _execute_stop(self):
        pass
