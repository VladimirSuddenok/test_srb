from aiohttp.web import View, Response

class EventView(View):
    async def get(self):
        msg = "echo: %s" % str(self.request)
        return Response(text=msg)

    #async def post(self):
    #    return await post_resp(self.request)