# boot.py -- run on boot-up
from sys import path
path.append("mipy_lib")
path.append("web")
import micropython
import uasyncio as asyncio
import time # type: ignore
from mipy_lib.ntptime_tz import settime_tz
#import ntptime_tz
import logging
# from lib.tail_log_handler import TailLogHandler
from mipy_lib.log_retainer import LogRetainHandler, LogRetainFilter

micropython.alloc_emergency_exception_buf(100)


import network
network.WLAN(network.AP_IF).active(False)
wlan = network.WLAN(network.STA_IF)


def configureLogging():
    
    retainer = LogRetainHandler()
    filter = LogRetainFilter(name="FilaChk", level=logging.INFO,count=10)
    retainer.addFilter(filter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    logger:logging.Logger = logging.getLogger("root")
    logger.addHandler(retainer)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.INFO)
    logging.defaultFmt = logging.Formatter("%(asctime)s [%(name)s %(levelname)s] %(message)s")
    streamHandler.setFormatter(logging.defaultFmt)
    retainer.setFormatter(logging.defaultFmt)


def connectWifi():
    from mipy_lib.veil import Veil
    # network.hostname("")
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.active(False)
        wlan.active(True)
        wlan.config(pm=wlan.PM_PERFORMANCE)
        v = Veil("sysinfo")
        wlan.connect( v.get_value("ssid"), v.get_value("access"))
        tryCount = 0
        while not wlan.isconnected():
            # await asyncio.sleep_ms(250)
            time.sleep_ms(250)
            if wlan.isconnected():
                print(':', end='')
            else:
                print('.', end='')
            if tryCount > 4*60: # 1 min
                print()
                print("ERROR: Not able to establish wifi connection after 1 min. Abandon.")  
                try:
                    # wlan.disconnect()
                    wlan.active(False)
                except Exception as e:
                    print("--->",e)
                return
            tryCount += 1
    print()
    # print('Unique ix: ', list(machine.unique_id()))
    print('Mac: ', list(wlan.config('mac')))
    print('network config:', wlan.ifconfig())




configureLogging()
connectWifi()
#ntptime_tz.settime()
settime_tz("GMT+1",True)