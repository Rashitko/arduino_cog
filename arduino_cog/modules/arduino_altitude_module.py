from up.base_started_module import BaseStartedModule
from up.commands.altitude_command import AltitudeCommand
from up.commands.command import BaseCommandHandler

from arduino_cog.modules.arduino_module import ArduinoModule


class ArduinoAltitudeCommandHandler(BaseCommandHandler):
    def __init__(self, callbacks):
        super().__init__()
        self.__callbacks = callbacks

    def run_action(self, command):
        altitude = command.data.get('altitude', None)
        if altitude:
            self.__callbacks.altitude = altitude


class ArduinoAltitudeModule(BaseStartedModule):
    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__altitude = 0
        self.__arduino_module = None
        self.__altitude_change_handle = None

    def _execute_start(self):
        super()._execute_start()
        self.__arduino_module = self.up.get_module(ArduinoModule.__name__)
        if self.arduino_module is None:
            self.logger.critical("Arduino Module not found")
            raise ValueError("Arduino Module not found")
        self.__altitude_change_handle = self.up.command_executor.register_command(AltitudeCommand.NAME,
                                                                                  ArduinoAltitudeCommandHandler(self))
        return True

    def _execute_stop(self):
        super()._execute_stop()
        self.up.command_executor.unregister_command(AltitudeCommand.NAME, self.__altitude_change_handle)

    @property
    def altitude(self):
        return self.__altitude

    @altitude.setter
    def altitude(self, value):
        if self.__altitude != value:
            self.arduino_module.send_altitude(value)
        self.__altitude = value

    @property
    def arduino_module(self):
        return self.__arduino_module
