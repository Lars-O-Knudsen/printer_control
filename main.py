from web.server import webserver
from web import routes
import gc
gc.collect()    

import time
import logging
import asyncio
from machine import Pin
# import requests

from filament_checker import FilamentChecker
from power_controller import PowerController
from sys_params import sysParams
gc.collect()

sysParams['simulationMode'] = True


logging.info( f"======== Boot -- {'Simulation Mode' if sysParams['simulationMode'] else 'Production'}  --  ram {gc.mem_free()} free / {gc.mem_alloc()} alloc ========")


# initialise filament checker
# filament_pin: Pin = Pin(16, Pin.IN, pull=Pin.PULL_DOWN,value=0)
filament_pin: Pin = Pin(5, Pin.IN, pull=Pin.PULL_DOWN,value=0)
filament_checker:FilamentChecker = FilamentChecker(filament_pin,2000,2,verbose=False)

# initialise printer power controller
# power_pin: Pin = Pin(17,Pin.OUT, value=0)
power_pin: Pin = Pin(6,Pin.OUT, value=0)
power_ctrl: PowerController = PowerController(power_pin)


app:webserver = webserver(context={"filament_checker":filament_checker,"power_controller":power_ctrl})
routes.setupRoutes( app)




try:
    # def handle_exception(loop, context):
    #     # uncaught exceptions end up here
    #     import sys
    #     print("global exception handler:", context)
    #     sys.print_exception(context["exception"])
    #     sys.exit()

    loop = asyncio.get_event_loop()
    # loop.set_exception_handler(handle_exception)

    filament_checker.start()

    # loop.create_task(relay_task())

    print("Starting web server ...")
    app.run(host='0.0.0.0', port=80, loop_forever=False)    # installs server as a task itself

    loop.run_forever()
except KeyboardInterrupt:
    print("Keyboard interrupt detected.")
finally:
    print("Shut down")
    # app.shutdown()
    asyncio.new_event_loop()

