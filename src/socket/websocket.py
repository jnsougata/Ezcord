import json
import time
import asyncio
import aiohttp
from src.listener.Listen import Listener



class Websocket:
    def __init__(
            self,
            secret: str,
            prefix:str,
            bucket: list,
    ):
        self.ws = None
        self.session = None
        self.secret = secret
        self.start_time = 0
        self.ack_time = 0
        self.interval = 0
        self.bucket = bucket
        self.prefix = prefix



    async def getGateway(self):
        URL = "https://discordapp.com/api/gateway"
        response = await self.session.get(URL)
        TEMP = await response.json()
        return TEMP['url']


    async def send_heartbeat(self, data: dict):
        if data["op"] == 10:
            self.interval = data['d']['heartbeat_interval']
            asyncio.ensure_future(
                self.heartBeat(self.interval)
            )


    async def heartbeat_ack(self, data: dict):
        if data['op'] == 11:
            self.ack_time = time.time() * 1000
            print(f'[ Latency: {self.ack_time - self.start_time}ms ]')


    async def heartBeat(self, interval):
        while True:
            await asyncio.sleep(interval / 1000)
            self.start_time = time.time() * 1000
            await self.ws.send_json(
                {
                    "op": 1,
                    "d": None
                }
            )


    async def handler(self, url):
        async with self.session.ws_connect(
                f"{url}?v=9&encoding=json") as ws:

            async for msg in ws:
                self.ws = ws
                data = json.loads(msg.data)

                listener = Listener(
                    response = data,
                    socket = self.ws,
                    secret = self.secret,
                    session = self.session,
                    bucket = self.bucket
                )
                await listener.run()
                await self.send_heartbeat(data)
                await self.heartbeat_ack(data)


    async def connect(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            gateway = await self.getGateway()
            await self.handler(gateway)
