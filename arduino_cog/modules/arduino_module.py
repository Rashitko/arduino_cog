import struct
from time import sleep

from serial_provider.modules.serial_module import SerialProvider
from up.base_started_module import BaseStartedModule
from up.commands.heading_command import HeadingCommand


class ArduinoModule(BaseStartedModule):
    LOAD_ORDER = SerialProvider.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__serial_module = None
        self._load_order = SerialProvider.LOAD_ORDER

    def _execute_initialization(self):
        self.__serial_module = self.up.get_module(SerialProvider.__name__)
        if self.__serial_module is None:
            self.logger.critical('SerialProvider not available')
            raise ValueError('SerialProvider not available')
        self.__serial_module.port = '/dev/cu.usbmodem1421'
        self.__serial_module.baud_rate = 9600
        self.serial_module.add_handler(ArduinoCommands.START_COMMAND_TYPE, self.__handle_start)
        self.serial_module.add_handler(ArduinoCommands.ARM_COMMAND_TYPE, self.__handle_arming_changed, 0, True)
        self.serial_module.add_handler(ArduinoCommands.DISARM_COMMAND_TYPE, self.__handle_arming_changed, 0, False)

    def _execute_start(self):
        if self.serial_module.started:
            self.serial_module.send_command(ArduinoCommands.START_COMMAND_TYPE)
            self.serial_module.send_command(ArduinoCommands.DISARM_COMMAND_TYPE)
        return self.serial_module.started

    def _execute_stop(self):
        pass

    def send_altitude(self, altitude):
        data = struct.pack("h", altitude)
        self.serial_module.send_command(ArduinoCommands.ALTITUDE_COMMAND_TYPE, data)

    def send_heading(self, heading, mode):
        if mode == HeadingCommand.SET_MODE_REQUIRED:
            data = struct.pack("!h", round(heading))
            self.send_arduino_command(ArduinoCommands.REQUIRED_HEADING_COMMAND_TYPE, data)
        elif mode == HeadingCommand.SET_MODE_ACTUAL:
            data = struct.pack("!h", round(heading))
            self.send_arduino_command(ArduinoCommands.ACTUAL_HEADING_COMMAND_TYPE, data)

    def send_location(self, lat, lon):
        data = struct.pack("!ff", lat, lon)
        self.send_arduino_command(ArduinoCommands.LOCATION_COMMAND_TYPE, data)

    def __handle_start(self, payload):
        self.logger.info('Arduino started')

    def __handle_arming_changed(self, armed, sth):
        if armed:
            self.logger.warn("Arduino ARMED")
        else:
            self.logger.warn("Arduino DISARMED")

    @property
    def serial_module(self) -> SerialProvider:
        return self.__serial_module


class ArduinoCommands:
    DISARM_COMMAND_TYPE = 'd'
    ARM_COMMAND_TYPE = 'a'
    START_COMMAND_TYPE = 's'
    ALTITUDE_COMMAND_TYPE = 'h'
    FLIGHT_MODE_SET_COMMAND_TYPE = 'M'
    FLIGHT_MODE_GET_COMMAND_TYPE = 'm'
    LOCATION_COMMAND_TYPE = 'l'
    ACTUAL_HEADING_COMMAND_TYPE = 'b'
    REQUIRED_HEADING_COMMAND_TYPE = 'B'
