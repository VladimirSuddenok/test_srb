''' Endpoint '''

import asyncio
#from settings import Setup
#from classes.server import Server 

version = "0.001.001"

async def printer():
    print("start")
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