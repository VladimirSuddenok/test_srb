from aiohttp.web import View, Response, json_response
from typing import Type
from classes.model import Patterns

from logging import getLogger

logger = getLogger(__name__)

class EventView(View):
    ''' View '''

    async def get(self) -> Type["Response"]:
        ''' echo test '''
        msg = "echo: %s" % str(self.request)
        return Response(text=msg)

    async def post(self) -> Type["json_response"]:
        ''' Processing of POST-request '''
        msg = await self._parse_msg()
        result = {"rule_name": ""}

        if not msg:
            result["rule_name"] = None
            result["error"] = "there is no parameter 'event'"

        else:
            status, message = await Patterns.check_message(msg=msg)
            result["rule_name"] = message if status else None
        
        msg = "EventView - post - result data - %s" % str(result)
        logger.debug(msg)

        return json_response(data=result)

    async def _parse_msg(self) -> str:
        ''' Look up parameter 'event' '''
        data = await self.request.post()

        msg = "EventView - post - raw_post data - %s" % str(data)
        logger.debug(msg)

        return data.get("event", "")