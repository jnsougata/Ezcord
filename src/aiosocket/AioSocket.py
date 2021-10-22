import time
import json
import aiohttp
import asyncio
from src.utils.Entity import Context
from src.slash.SlashHandler import Slash
from src.slash.SlashEvent import SlashContext



class Socket:
    def __init__(
            self,
            secret: str,
    ):
        #args
        self.secret = secret


        #latency
        self.start_time = 0
        self.ack_time = 0

        #use for post only
        self.auth_header = {"Authorization": f"Bot {secret}"}

        #socket properties
        self.ws = None
        self.session = None
        self.interval = None


    async def send_message(self, content:str, channel_id: int):
        await self.session.post(
            f'https://discord.com/api/v9/channels/{channel_id}/messages',
            data = {"content": content},
            headers = self.auth_header
        )




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


    async def heartBeat(self, interval):
        while True:
            await asyncio.sleep(interval / 1000)
            await self.ws.send_json(
                {
                    "op": 1,
                    "d": None
                }
            )
            self.start_time = time.time() * 1000


    async def handler(self, url):
        async with self.session.ws_connect(
                f"{url}?v=9&encoding=json") as ws:

            async for msg in ws:
                self.ws = ws
                data = json.loads(msg.data)

                # OP Code checking

                if data["op"] == 0: #dispatch
                    print(f'[ {data["t"]} ]')
                    raw = data['d']
                    print(raw)
                    event = data['t']

                    if event == 'INTERACTION_CREATE':
                        action = SlashContext(raw)
                        body = await action.buildBody()
                        await action.postCallback(self.session, body)

                    if event == 'MESSAGE_CREATE':
                        ctx = Context(raw)
                        if ctx.author.id != 874663148374880287:
                            if ctx.message.lower() == 'hi':
                                await self.send_message(
                                    content = f"Hi...{ctx.author.mention}, this is an automate messgae!",
                                    channel_id = ctx.channel_id
                                )


                elif data["op"] == 10:
                    self.interval = data['d']['heartbeat_interval']
                    asyncio.ensure_future(
                        self.heartBeat(self.interval)
                    )
                    await ws.send_json(
                        {
                            "op": 2,
                            "d": {
                                "token": self.secret,
                                "intents": 513,
                                "properties": {
                                    '$os': "ios",
                                    '$browser': 'Discord iOS',
                                    '$device': 'discord.py',
                                    '$referrer': '',
                                    '$referring_domain': ''
                                }
                            }
                        }
                    )


                elif data["op"] == 11:
                    self.ack_time = time.time() * 1000
                    print(f'[ Latency: {self.ack_time - self.start_time}ms ]')

                else:
                    print(data)
