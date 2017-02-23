import os

import yaml
from up.base_started_module import BaseStartedModule
from up.registrar import UpRegistrar

from arduino_cog.commands.pid_tunings_command import PIDTuningsCommand, PIDTuningsCommandHandler
from arduino_cog.modules.arduino_module import ArduinoModule
from arduino_cog.registrar import Registrar


class PIDTuningsProvider(BaseStartedModule):
    LOAD_ORDER = ArduinoModule.LOAD_ORDER + 1

    def __init__(self):
        super().__init__()
        self.__pid_tunings_handler = None
        self.__rate_pids = None
        self.__stab_pids = None
        self.__arduino_module = None

    def _execute_initialization(self):
        super()._execute_initialization()

    def _execute_start(self):
        super()._execute_start()
        self.__arduino_module = self.up.get_module(ArduinoModule)
        if self.__arduino_module is None:
            self.logger.critical("Arduino Module not found")
            raise ValueError("Arduino Module not found")
        self.__pid_tunings_handler = self.up.command_executor.register_command(PIDTuningsCommand.NAME,
                                                                               PIDTuningsCommandHandler(self))
        self.__send_saved_pids()
        return True

    def _execute_stop(self):
        super()._execute_stop()
        if self.__pid_tunings_handler:
            self.up.command_executor.unregister_command(PIDTuningsCommand.NAME, self.__pid_tunings_handler)
        self.__save_pids()

    def on_pids_requested(self):
        self.__arduino_module.request_pids()

    def _on_pids_changed(self):
        self.__arduino_module.send_pids(self.pids)

    def load(self):
        return True

    def __send_saved_pids(self):
        config_path = os.path.join(os.getcwd(), UpRegistrar.CONFIG_PATH, Registrar.PIDS_CONFIG_FILE_NAME)
        if os.path.isfile(config_path):
            with open(config_path) as f:
                config = yaml.load(f)
                self.pids = {
                    PIDTuningsCommand.RATE_PIDS_KEY: config.get('rate'),
                    PIDTuningsCommand.STAB_PIDS_KEY: config.get('stabilize')
                }

    def __save_pids(self):
        config_path = os.path.join(os.getcwd(), UpRegistrar.CONFIG_PATH, Registrar.PIDS_CONFIG_FILE_NAME)
        with open(config_path, 'w+') as f:
            pids = {
                'rate': self.pids[PIDTuningsCommand.RATE_PIDS_KEY],
                'stabilize': self.pids[PIDTuningsCommand.STAB_PIDS_KEY]
            }
            self.logger.debug("Saving pids to pids.yml")
            yaml.dump(pids, f)

    @property
    def pids(self):
        return {'ratePIDs': self.rate_pids, 'stabPIDs': self.stab_pids}

    @pids.setter
    def pids(self, value):
        self.rate_pids = value[PIDTuningsCommand.RATE_PIDS_KEY]
        self.stab_pids = value[PIDTuningsCommand.STAB_PIDS_KEY]
        self._on_pids_changed()

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
