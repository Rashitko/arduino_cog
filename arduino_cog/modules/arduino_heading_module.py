from up.base_started_module import BaseStartedModule
from up.commands.heading_command import HeadingCommand
from up.commands.command import BaseCommandHandler

from arduino_cog.modules.arduino_module import ArduinoModule


class ArduinoHeadingCommandHandler(BaseCommandHandler):
    def __init__(self, callbacks):
        super().__init__()
        self.__callbacks = callbacks

    def run_action(self, command):
        heading = command.data.get('heading', None)
        mode = command.data.get('mode', None)
        if heading:
            self.__callbacks.new_heading(heading, mode)


class ArduinoHeadingModule(BaseStartedModule):
    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__arduino_module = None
        self.__heading_change_handle = None

    def _execute_start(self):
        super()._execute_start()
        self.__arduino_module = self.up.get_module(ArduinoModule.__name__)
        if self.arduino_module is None:
            self.logger.critical("Arduino Module not found")
            raise ValueError("Arduino Module not found")
        self.__heading_change_handle = self.up.command_executor.register_command(HeadingCommand.NAME,
                                                                                  ArduinoHeadingCommandHandler(self))
        return True

    def _execute_stop(self):
        super()._execute_stop()
        self.up.command_executor.unregister_command(HeadingCommand.NAME, self.__heading_change_handle)

    def new_heading(self, heading, mode):
        self.arduino_module.send_heading(heading, mode)

    @property
    def arduino_module(self) -> ArduinoModule:
        return self.__arduino_module
