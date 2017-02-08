from up.commands.command import BaseCommand, BaseCommandHandler


class ArduinoPanicCommand(BaseCommand):
    NAME = 'load_guard.panic'

    PANIC_KEY = 'panic'

    def __init__(self):
        super().__init__(ArduinoPanicCommand.NAME)


class ArduinoPanicCommandHandler(BaseCommandHandler):
    def __init__(self, arduino_module):
        super().__init__()
        self.__arduino_module = arduino_module

    def run_action(self, command):
        in_panic = command.data.get(ArduinoPanicCommand.PANIC_KEY, None)
        if in_panic is not None:
            self.__arduino_module.send_panic(in_panic)
