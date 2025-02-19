

import logging
from web.server import webserver, request, response
# from web import webutils
# from lib.tail_log_handler import TailLogHandler
from lib.log_retainer import LogRetainHandler
from sys_params import sysParams


def setupRoutes( app:webserver ):

    logger:logging.Logger = logging.getContextLogger( "websrv", base="root")

    apiRoute = "/api"

    # add service classes
    app.add_resource( app.context["filament_checker"], apiRoute + "/filamentState")
    app.add_resource( app.context["power_controller"], apiRoute + "/powerControl")

    logRetainers = [h for h in logger.handlers if isinstance( h, LogRetainHandler)]
    print(logRetainers, len(logRetainers))
    if len(logRetainers) > 0:
        app.add_resource( logRetainers[0], apiRoute + "/log", logger=logger)


    # add index path
    @app.route('/',methods=["GET"])
    async def index( req:request,resp:response):
        logger.info("Get Root")
        await resp.send_file("web/root.html",'text/html; charset="utf-8"',"utf-8",max_age=0)


    @app.resource(apiRoute + "/mode", method="GET")
    def getSimulationMode( data ):
        simul = sysParams.get("simulationMode")
        res = "SIMULATION" if simul else "PRODUCTION"
        logger.info(f"getSimulationMode requested. Mode:{res}")
        return { "mode": res }
      

    @app.resource(apiRoute + "/toggleMode", method="POST")
    def toggleSimulationMode( data ):
        simul = sysParams.get("simulationMode")
        simul = not simul
        sysParams["simulationMode"] = simul
        res = "SIMULATION" if simul else "PRODUCTION"
        logger.info(f"Toggle Simulation Mode. New state :{simul}")
        return { "mode": res }
      


    async def send_file(req:request, resp:response, path:str, fn:str):
        # Send file fn
        if   fn.endswith(".js"):        ct="text/javascript"
        elif fn.endswith(".html"):     ct="text/html"
        elif fn.endswith(".css"):       ct="text/css"
        logger.info(f"Request for static file: {fn}")
        await resp.send_file(f'{path}/{fn}', content_type=ct,max_age=0)

    # static files from web/
    @app.route('/web/<fn>')
    async def static_file(req:request, resp:response, fn:str):
        await send_file( req, resp, "web", fn)
    @app.route('/web/comp/<fn>')
    async def static_comp(req:request, resp:response, fn:str):
        await send_file( req, resp, "web/comp", fn)


    # @app.route(f"{apiRoute}/old/log")
    # async def getLogTail(req:request, resp:response):
    #     tailHandler = [h for h in logger.handlers if isinstance( h, TailLogHandler)]
    #     # tailHandler = None
    #     print(">", tailHandler)
    #     if len(tailHandler) > 0:
    #         tailHandler = tailHandler[0]
    #         logger.info(f"Tail logger contains last {len(tailHandler.tail)} of {tailHandler.logCount} logged items.")
    #         for idx, line in enumerate(reversed(tailHandler.tail)):
    #             await resp.send( f"{tailHandler.logCount-idx}> {line}\n")
    #     else:
    #         logger.warning("No TailLoghandler found, yet a path was setup.")
    #         await resp.send( "No history handler found.")

    
    # def _getTailLogHandler() -> TailLogHandler|None:
    #     tailHandler = [h for h in logger.handlers if isinstance( h, TailLogHandler)]
    #     return tailHandler[0] if len(tailHandler) > 0 else None
        

