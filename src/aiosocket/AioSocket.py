import json
import aiohttp
from src.listener.Listen import Listener



class Socket:
    def __init__(
            self,
            secret: str,
    ):
        self.ws = None
        self.session = None
        self.secret = secret



    async def getGateway(self):
        URL = "https://discordapp.com/api/gateway"
        response = await self.session.get(URL)
        TEMP = await response.json()
        return TEMP['url']


    async def connect(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            gateway = await self.getGateway()
            await self.handler(gateway)


    async def handler(self, url):
        async with self.session.ws_connect(
                f"{url}?v=9&encoding=json") as ws:

            async for msg in ws:
                self.ws = ws
                data = json.loads(msg.data)

                listener = Listener(
                    secret = self.secret,
                    response = data,
                    session = self.session,
                    socket = self.ws
                )
                await listener.run()



