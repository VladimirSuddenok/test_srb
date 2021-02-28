''' Endpoint '''

import asyncio
from settings import Setup

from logging import getLogger
from datetime import datetime

from classes.server import Server
from classes.model import Patterns

version = "0.007.005"

def start_log() -> int:
    ''' Write start log-information '''
    logger = getLogger(__name__)
    logger.info("*"*100 + "\n")

    template = "start application - v.{version} - {date}"
    msg = template.format(version=version, date=datetime.now())
    logger.info(msg)

    return 0

async def main():
    ''' asyncio endpoint '''
    await Setup.setup()
    server_runner = Server().get_runner()

    start_log()
    await asyncio.gather(
        Patterns.load_patterns(),
        server_runner
    )

if __name__ == "__main__":
    asyncio.run(main())