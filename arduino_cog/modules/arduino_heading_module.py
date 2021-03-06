from up.commands.heading_command import HeadingCommand
from up.modules.up_heading_provider import UpHeadingProvider

from arduino_cog.modules.arduino_module import ArduinoModule


class ArduinoHeadingModule(UpHeadingProvider):
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

    def _on_actual_heading_changed(self, new_actual_heading):
        super()._on_actual_heading_changed(new_actual_heading)
        self.arduino_module.send_heading(new_actual_heading, HeadingCommand.SET_MODE_ACTUAL)

    def _on_required_heading_changed(self, new_required_heading):
        super()._on_actual_heading_changed(new_required_heading)
        self.arduino_module.send_heading(new_required_heading, HeadingCommand.SET_MODE_REQUIRED)

    def load(self):
        return True

    @property
    def arduino_module(self) -> ArduinoModule:
        return self.__arduino_module
