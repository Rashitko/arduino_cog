import os
import struct

import yaml
from serial_provider_cog.modules.serial_module import SerialProvider
from up.base_started_module import BaseStartedModule
from up.commands.heading_command import HeadingCommand
from up.modules.up_orientation_provider import UpOrientationProvider
from up.providers.base_rx_provider import BaseRXProvider
from up.registrar import UpRegistrar

from arduino_cog.commands.arduino_panic_command import ArduinoPanicCommand, ArduinoPanicCommandHandler
from arduino_cog.commands.pid_tunings_command import PIDTuningsCommand, PIDTuningsValuesCommandFactory
from arduino_cog.registrar import Registrar


class ArduinoModule(BaseStartedModule):
    LOAD_ORDER = SerialProvider.LOAD_ORDER + 1

    PANIC_DELAY = 150
    NORMAL_DELAY = 50

    def __init__(self):
        super().__init__()
        self.__serial_module = None
        self.__orientation_provider = None
        self.__panic_handle = None
        self._load_order = SerialProvider.LOAD_ORDER

    def _execute_initialization(self):
        self.__serial_module = self.up.get_module(SerialProvider)
        if self.__serial_module is None:
            self.logger.critical('SerialProvider not available')
            raise ValueError('SerialProvider not available')
        port, baudrate = self.__read_config()
        if port is not None and baudrate is not None:
            self.__serial_module.port = port
            self.__serial_module.baud_rate = baudrate
            self.serial_module.add_handler(ArduinoCommands.ERROR_COMMAND_TYPE, self.__handle_error, 1)
            self.serial_module.add_handler(ArduinoCommands.START_COMMAND_TYPE, self.__handle_start)
            self.serial_module.add_handler(ArduinoCommands.ARM_COMMAND_TYPE, self.__handle_arming_changed, 0, True)
            self.serial_module.add_handler(ArduinoCommands.DISARM_COMMAND_TYPE, self.__handle_arming_changed, 0, False)
            self.serial_module.add_handler(ArduinoCommands.ACTUAL_HEADING_COMMAND_TYPE, self.__handle_heading, 2,
                                           ArduinoCommands.ACTUAL_HEADING_COMMAND_TYPE)
            self.serial_module.add_handler(ArduinoCommands.REQUIRED_HEADING_COMMAND_TYPE, self.__handle_heading, 2,
                                           ArduinoCommands.REQUIRED_HEADING_COMMAND_TYPE)
            self.serial_module.add_handler(ArduinoCommands.LOCATION_COMMAND_TYPE, self.__handle_location, 8)
            self.serial_module.add_handler(ArduinoCommands.ALTITUDE_COMMAND_TYPE, self.__handle_altitude, 2)
            self.serial_module.add_handler(ArduinoCommands.ORIENTATION_COMMAND_TYPE, self.__handle_orientation, 12)
            self.serial_module.add_handler(ArduinoCommands.PANIC_COMMAND_TYPE, self.__handle_panic, 3)
            self.serial_module.add_handler(ArduinoCommands.PID_TUNINGS, self.__handle_pid_tunings, 48, False)
            self.serial_module.add_handler(ArduinoCommands.PID_TUNINGS_REQUEST, self.__handle_pid_tunings, 48, True)
            self.serial_module.add_handler(ArduinoCommands.RX_VALUES, self.__handle_rx_values, 8)
        else:
            self.logger.critical('Port and baudrate not set, set them in %s' % Registrar.CONFIG_FILE_NAME)

        self.__orientation_provider = self.up.get_module(UpOrientationProvider)
        if self.__orientation_provider is None:
            self.logger.critical('OrientationProvider not available')
            raise ValueError('OrientationProvider not available')

        self.__rx_provider = self.up.get_module(BaseRXProvider)
        if self.__rx_provider is None:
            self.logger.critical('RXProvider not available')
            raise ValueError('RXProvider not available')

    def _execute_start(self):
        super()._execute_start()
        self.__panic_handle = self.up.command_executor.register_command(ArduinoPanicCommand.NAME,
                                                                        ArduinoPanicCommandHandler(self))
        return self.serial_module.started

    def _execute_stop(self):
        super()._execute_start()
        if self.__panic_handle is not None:
            self.up.command_executor.unregister_command(ArduinoPanicCommand.NAME, self.__panic_handle)

    def load(self):
        return True

    def send_altitude(self, altitude):
        data = struct.pack("h", altitude)
        self.serial_module.send_command(ArduinoCommands.ALTITUDE_COMMAND_TYPE, data)

    def send_heading(self, heading, mode):
        if mode == HeadingCommand.SET_MODE_REQUIRED:
            data = struct.pack("!h", round(heading))
            self.serial_module.send_command(ArduinoCommands.REQUIRED_HEADING_COMMAND_TYPE, data)
        elif mode == HeadingCommand.SET_MODE_ACTUAL:
            data = struct.pack("!h", round(heading))
            self.serial_module.send_command(ArduinoCommands.ACTUAL_HEADING_COMMAND_TYPE, data)

    def send_location(self, lat, lon):
        data = struct.pack("!ff", lat, lon)
        self.serial_module.send_command(ArduinoCommands.LOCATION_COMMAND_TYPE, data)

    def send_panic(self, in_panic):
        if in_panic:
            required_delay = self.PANIC_DELAY
            self.logger.warning('Sending PANIC ENTER to Arduino')
        else:
            required_delay = self.NORMAL_DELAY
            self.logger.info('Sending PANIC LEAVE to Arduino')
        data = struct.pack("!?h", in_panic, required_delay)
        self.serial_module.send_command(ArduinoCommands.PANIC_COMMAND_TYPE, data)

    def send_pids(self, pids):
        data = []
        rate_pids = pids.get(PIDTuningsCommand.RATE_PIDS_KEY)
        if rate_pids:
            data.append(rate_pids[PIDTuningsCommand.AILERONS_KEY][PIDTuningsCommand.P_KEY])
            data.append(rate_pids[PIDTuningsCommand.AILERONS_KEY][PIDTuningsCommand.I_KEY])
            data.append(rate_pids[PIDTuningsCommand.AILERONS_KEY][PIDTuningsCommand.D_KEY])
            data.append(rate_pids[PIDTuningsCommand.ELEVATOR_KEY][PIDTuningsCommand.P_KEY])
            data.append(rate_pids[PIDTuningsCommand.ELEVATOR_KEY][PIDTuningsCommand.I_KEY])
            data.append(rate_pids[PIDTuningsCommand.ELEVATOR_KEY][PIDTuningsCommand.D_KEY])
        stab_pids = pids.get(PIDTuningsCommand.STAB_PIDS_KEY)
        if stab_pids:
            data.append(stab_pids[PIDTuningsCommand.AILERONS_KEY][PIDTuningsCommand.P_KEY])
            data.append(stab_pids[PIDTuningsCommand.AILERONS_KEY][PIDTuningsCommand.I_KEY])
            data.append(stab_pids[PIDTuningsCommand.AILERONS_KEY][PIDTuningsCommand.D_KEY])
            data.append(stab_pids[PIDTuningsCommand.ELEVATOR_KEY][PIDTuningsCommand.P_KEY])
            data.append(stab_pids[PIDTuningsCommand.ELEVATOR_KEY][PIDTuningsCommand.I_KEY])
            data.append(stab_pids[PIDTuningsCommand.ELEVATOR_KEY][PIDTuningsCommand.D_KEY])
        if self.started:
            self.logger.info("Sending PIDs: %s" % data)
            self.serial_module.send_command(ArduinoCommands.PID_TUNINGS, struct.pack("!ffffffffffff", *data))
        else:
            self.logger.error("Not started, cannot send PIDs")

    def request_pids(self):
        if self.started:
            self.logger.info("Requesting PIDs")
            self.serial_module.send_command(ArduinoCommands.PID_TUNINGS_REQUEST)
        else:
            self.logger.error("Not started, cannot request PIDs")

    @staticmethod
    def __read_config():
        config_path = os.path.join(os.getcwd(), UpRegistrar.CONFIG_PATH, Registrar.CONFIG_FILE_NAME)
        port = None
        baud_rate = None
        if os.path.isfile(config_path):
            with open(config_path) as f:
                config = yaml.load(f)
                port = config.get(Registrar.PORT_KEY, None)
                baud_rate = config.get(Registrar.BAUD_RATE_KEY)
        return port, baud_rate

    def __handle_start(self, payload):
        self.logger.info('Arduino started')

    def __handle_arming_changed(self, armed, sth):
        if armed:
            self.logger.warn("Arduino ARMED")
        else:
            self.logger.warn("Arduino DISARMED")

    def __handle_heading(self, payload, mode):
        heading, = struct.unpack('!h', payload)
        if mode == ArduinoCommands.ACTUAL_HEADING_COMMAND_TYPE:
            readable_mode = 'Actual'
        elif mode == ArduinoCommands.REQUIRED_HEADING_COMMAND_TYPE:
            readable_mode = 'Required'
        else:
            readable_mode = 'Unknown mode'
        message = '%s heading %s confirmed' % (readable_mode, heading)
        self.logger.debug(message)

    def __handle_location(self, payload):
        lat, lon = struct.unpack("!ff", payload)
        self.logger.debug('Location %.6f %.6f confirmed' % (lat, lon))

    def __handle_altitude(self, payload):
        altitude, = struct.unpack("!h", payload)
        self.logger.debug('Altitude %s confirmed' % altitude)

    def __handle_orientation(self, payload):
        yaw, pitch, roll = struct.unpack("!fff", payload)
        self.__orientation_provider.yaw = yaw
        self.__orientation_provider.pitch = pitch
        self.__orientation_provider.roll = roll

    def __handle_error(self, payload):
        rejected, = struct.unpack("!c", payload)
        self.logger.error("Arduino rejected command %s" % rejected)

    def __handle_panic(self, payload):
        in_panic, delay = struct.unpack("!?h", payload)
        self.logger.debug("Arduino confirmed PANIC DELAY of %sms" % delay)

    def __handle_pid_tunings(self, payload, is_request):
        pids = list(struct.unpack("!ffffffffffff", payload))
        pids = [round(x, 2) for x in pids]
        if is_request:
            self.logger.info("PIDs settings: %s" % pids)
            cmd = PIDTuningsValuesCommandFactory.create(pids)
            self.up.mission_control_provider.send_command(cmd)
        else:
            self.logger.debug("Arduino confirmed PIDs: %s" % pids)

    def __handle_rx_values(self, payload):
        ail, ele, thr, rud = struct.unpack("!hhhh", payload)
        self.__rx_provider.set_channels(self.__rx_provider.create_channels_values(ail, ele, thr, rud))

    @property
    def telemetry_content(self):
        return {
            'arduino': {
                'connected': self.connected
            }
        }

    @property
    def serial_module(self) -> SerialProvider:
        return self.__serial_module

    @property
    def connected(self):
        return self.__serial_module.connected


class ArduinoCommands:
    ERROR_COMMAND_TYPE = '!'
    DISARM_COMMAND_TYPE = 'd'
    ARM_COMMAND_TYPE = 'a'
    START_COMMAND_TYPE = 's'
    ALTITUDE_COMMAND_TYPE = 'h'
    FLIGHT_MODE_SET_COMMAND_TYPE = 'M'
    FLIGHT_MODE_GET_COMMAND_TYPE = 'm'
    LOCATION_COMMAND_TYPE = 'l'
    ACTUAL_HEADING_COMMAND_TYPE = 'b'
    REQUIRED_HEADING_COMMAND_TYPE = 'B'
    ORIENTATION_COMMAND_TYPE = 'o'
    PANIC_COMMAND_TYPE = 'p'
    PID_TUNINGS = 't'
    PID_TUNINGS_REQUEST = 'T'
    RX_VALUES = 'r'
