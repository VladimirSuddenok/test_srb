from classes.parents_classes.base_class import BaseClass, debug_logger_inst
from aiohttp import web
from classes.view import EventView

from logging import getLogger

logger = getLogger(__name__)

class Server(BaseClass):
    '''  '''
    parameters = ["host", "port"]
    
    @debug_logger_inst
    def __init__(self):
        '''  '''
        # here will be all application routes
        # type: get, post, put, view
        # template {"url": "your/url", "type": "view", "handler": your_handel}
        self._routes = [
            {"url": "/push_event", "type": "view", "handler": EventView},
        ]

    def _set_view(self, app) -> int:
        ''' build application routes '''
        for route in self._routes:
            buffer = []

            if route["type"] == "view":
                buffer.append(
                    web.view(route["url"], route["handler"])
                )
                
            app.add_routes(buffer)
        
        return 0

    @classmethod
    def get_runner(cls):
        ''' return coroutine for start server '''
        logger.debug("Server - get_runner - build aoihttp application")
        instance = Server()
        app = web.Application()

        instance._set_view(app=app)
        run_args = {"app": app, "host": cls.host, "port": cls.port}

        return web._run_app(**run_args)