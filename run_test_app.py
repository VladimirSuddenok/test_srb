''' Endpoint '''

import asyncio
#from settings import Setup
from classes.server import Server 

version = "0.001.001"

async def printer():
    settings = {"host": "127.0.0.1", "port": 8080}
    Server.set_cls_params(**settings)
    server_runner = Server.get_runner()
    print("server_run_cor", server_runner)
    await server_runner

    return 0

async def main():
    # settings up classes
    #s = Setup()
    # build server instances
    #server = Server()
    #start_func, args = server.get_runner()
    
    await asyncio.gather(
        printer()
        # print start log
        # run server
    )

if __name__ == "__main__":
    asyncio.run(main())