
from machine import Pin
import logging
from sys_params import sysParams

class PowerController:

    POWER_ON = 1
    POWER_OFF = 0
    POWER_TEXT = ("OFF","ON")

    def __init__(self, pin):
        self.pin:Pin = pin
        self._logger:logging.Logger = logging.getContextLogger("PowerCtrl")


    def get(self, data):
        state = self.POWER_TEXT[self.pin.value()]
        self._logger.info(f"Get/Power state requested, current state: {state}")
        return {"powerState": state}


    def post(self, data):
        self._logger.info(f"Post/Power state requested, Requested state: {data}")
        state = self.__textToState(data["powerState"])
        simul = sysParams.get("simulationMode")
        if simul:
            self._logger.warning("In SIMULATION mode, no REAL action taken")
        if state != self.pin.value():
            if not simul:
                self.pin.value(state)
        return {"powerState": self.POWER_TEXT[state]}

    def __textToState(self, txt:str) -> int:
        return self.POWER_OFF if txt == self.POWER_TEXT[self.POWER_OFF] else self.POWER_ON
    