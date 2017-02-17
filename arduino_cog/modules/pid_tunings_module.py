from up.base_started_module import BaseStartedModule

from arduino_cog.commands.pid_tunings_command import PIDTuningsCommand, PIDTuningsCommandHandler
from arduino_cog.modules.arduino_module import ArduinoModule


class PIDTuningsProvider(BaseStartedModule):

    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__pid_tunings_handler = None
        self.__rate_pids = None
        self.__stab_pids = None
        self.__nav_pids = None
        self.__arduino_module = None

    def _execute_initialization(self):
        super()._execute_initialization()

    def _execute_start(self):
        self.__arduino_module = self.up.get_module(ArduinoModule)
        if self.__arduino_module is None:
            self.logger.critical("Arduino Module not found")
            raise ValueError("Arduino Module not found")
        self.__pid_tunings_handler = self.up.command_executor.register_command(PIDTuningsCommand.NAME,
                                                                               PIDTuningsCommandHandler(self))
        return True

    def _execute_stop(self):
        super()._execute_stop()
        if self.__pid_tunings_handler:
            self.up.command_executor.unregister_command(PIDTuningsCommand.NAME, self.__pid_tunings_handler)

    def on_pids_requested(self):
        self.__arduino_module.request_pids()

    def load(self):
        return True

    @property
    def pids(self):
        return {'ratePIDs': self.rate_pids, 'stabPIDs': self.stab_pids, 'navPIDs': self.nav_pids}

    @pids.setter
    def pids(self, value):
        self.rate_pids = value['ratePIDs']
        self.stab_pids = value['stabPIDs']
        self.nav_pids = value['navPIDs']
        self.__arduino_module.send_pids(self.pids)

    @property
    def rate_pids(self):
        return self.__rate_pids

    @rate_pids.setter
    def rate_pids(self, value):
        self.__rate_pids = value

    @property
    def stab_pids(self):
        return self.__stab_pids

    @stab_pids.setter
    def stab_pids(self, value):
        self.__stab_pids = value

    @property
    def nav_pids(self):
        return self.__nav_pids

    @nav_pids.setter
    def nav_pids(self, value):
        self.__nav_pids = value
