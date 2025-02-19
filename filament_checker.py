
from machine import Pin
import asyncio
import logging
import requests
from sys_params import sysParams

class FilamentChecker:

    FILAMENT_OK=0
    FILAMENT_OUT=1
    FILAMENT_TXT = ("OK", "RUN OUT")
    OCTOPRINT_API_KEY="MmVRNXfxomie8fotBAFZyuR4ZBq7HrhIhlaL_2pVU3A"    
    OCTOPRINT_URL = "http://opi3b:5000/api/job"

    LOG_CHECK_INTERVAL = 30

    def __init__(self, pin:Pin, check_ms:int=1000, numConfirmChecks:int=2, verbose:bool=False):
        self.pin = pin
        self.check_ms = check_ms
        self.numConfirmChecks = numConfirmChecks
        self.state = None
        self._verbose = verbose
        self._logger:logging.Logger = logging.getContextLogger("FilaChk")

        self._logger.info(f"Filament checker initialsed. {'---SIMULATION MODE---' if sysParams.get('simulationMode') else ''}")


    def start(self):
        self._logger.info("Starting filament checker task")
        loop = asyncio.get_event_loop()
        loop.create_task(self.checker_task())


    def get(self, data):
        """Return current (last checked) state of filament sensor"""
        self._logger.info("Filament status requested")
        # jobState = self.octoprintJobState()
        # return {"filamentState": self.FILAMENT_TXT[self.state],
        #         "jobState": jobState["state"], 
        #         "fullJobState": jobState}
        return {"filamentState": self.FILAMENT_TXT[self.state]}

    def post(self, data):
        """Execute command on printer and return resulting state of filament sensor"""
        self._logger.info(f"Received command: {data}")
        return {"success":True, "data": self.get(None)}


    async def checker_task(self):
        old_state = self.pin.value()    # initial state of filament
        checks = 0
        check_count = 0
        while True:
            self.state = self.pin.value()
            stateChanged = self.state != old_state
            if self._verbose or stateChanged or (check_count % self.LOG_CHECK_INTERVAL == 0): 
                self._logger.info(f"checking filament: {self.FILAMENT_TXT[self.state]}   State Changed: {stateChanged}    #checks:{checks}")
            check_count += 1
            if stateChanged:
                checks += 1
                if checks >= self.numConfirmChecks:
                    if self.state == self.FILAMENT_OUT:
                        self._logger.info("Filament has run out!!")
                        #send pause
                        self.octoPrintPauseJob()
                    # else:
                    #     #send  resume, if auto start enabled
                    #     if fila_auto_start:
                    #         sendOctoPrintCommand("resume")
                    old_state = self.state
                    checks = 0
            else:
                checks = 0

            await asyncio.sleep_ms(self.check_ms)


    def octoprintJobState(self):
        self._logger.info(f"Getting Octoprint job state:  url:{self.OCTOPRINT_URL}")
        hdrs = {"X-Api-Key":f"{self.OCTOPRINT_API_KEY}"}
        resp: requests.Response = requests.get( self.OCTOPRINT_URL, headers=hdrs)
        data = resp.json()
        self._logger.info(f"Octoprint reply: {data}")
        return data


    def octoPrintPauseJob(self):
        payload = '{"command": "pause", "action":"pause"}'
        self._logger.info(f"Pausing Octoprint job:  payload:{payload}   url:{self.OCTOPRINT_URL}")
        if sysParams.get('simulationMode'):
            self._logger.warning("In SIMULATION mode, no request sent to Octoprint")
            return
        hdrs = {"Content-Type": "application/json", "X-Api-Key":f"{self.OCTOPRINT_API_KEY}"}
        resp: requests.Response = requests.post( self.OCTOPRINT_URL, headers=hdrs, data=payload)
        self._logger.info(f"Octoprint reply: {resp.json()}")
