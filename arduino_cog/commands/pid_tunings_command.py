from up.commands.command import BaseCommand, BaseCommandHandler


class PIDTuningsCommand(BaseCommand):
    NAME = "arduino.pids.tunings"

    REQUEST_KEY = 'request'
    PIDS_KEY = 'pids'

    NAV_PIDS_KEY = 'navPIDs'
    STAB_PIDS_KEY = 'stabPIDs'
    RATE_PIDS_KEY = 'ratePIDs'

    AILERONS_KEY = 'ailerons'
    ELEVATOR_KEY = 'elevator'

    P_KEY = 'p'
    I_KEY = 'i'
    D_KEY = 'd'

    def __init__(self):
        super().__init__(self.NAME)


class PIDTuningsCommandHandler(BaseCommandHandler):
    def __init__(self, provider):
        super().__init__()
        self.__provider = provider

    def run_action(self, command):
        is_request = command.data.get(PIDTuningsCommand.REQUEST_KEY)
        pids = command.data.get(PIDTuningsCommand.PIDS_KEY)
        if is_request:
            self.__provider.on_pids_requested()
        elif pids:
            self.__provider.pids = pids
        else:
            self.logger.error("Command arduino.pids.tunings does not contain request nor tunings data")