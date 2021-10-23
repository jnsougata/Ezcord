import json
import time
import asyncio
import aiohttp
from src.ez.map import Tweak
from src.ez.cmd import Executor
from src.ez.slash import SlashReply


class Receiver:

    def __init__(
            self,
            secret: str,
            response: dict,
            session: aiohttp.ClientSession,
            socket: aiohttp.ClientWebSocketResponse,
            bucket: list,
    ):
        self.data = response
        self.session = session
        self.auth_header = {"Authorization": f"Bot {secret}"}
        self.ws = socket
        self.start_time = 0
        self.ack_time = 0
        self.secret = secret
        self.bucket = bucket


    @property
    async def op(self):
        return int(self.data['op'])


    async def send_message(self, content:str, channel_id: int):
        await self.session.post(
            f'https://discord.com/api/v9/channels/{channel_id}/messages',
            data = {"content": content},
            headers = self.auth_header
        )


    async def run(self):
        CODE = await self.op
        DATA = self.data

        # RECEIVED DISPATCH
        if CODE == 0:
            EVENT = DATA['t']
            print(f'[ {EVENT} ]')
            RAW = DATA['d']
            print(DATA)

            # CHECKING EVENT TYPE

            if EVENT == 'INTERACTION_CREATE':
                slash = SlashReply(RAW)
                await slash.callback(self.session)

            if EVENT == 'MESSAGE_CREATE':
                ctx = Tweak(RAW)
                if ctx.author.id != 874663148374880287:
                    if ctx.message.lower() == 'hi':
                        await self.send_message(
                            content=f"Hi...{ctx.author.mention}, this is an automate messgae!",
                            channel_id=ctx.channel_id
                        )

                    PARSER = Executor(
                        ctx = ctx,
                        prefix = '-',
                        secret = self.secret,
                        bucket = self.bucket
                    )
                    body = await PARSER.process_message

                    if body:
                        await PARSER.post(
                            auth = self.auth_header,
                            body = body,
                            session = self.session
                        )

        # RECEIVED HELLO
        elif CODE == 10:

            # SENDING IDENTIFICATION PAYLOAD
            await self.ws.send_json(
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

        # HEART BEAT ACK
        elif CODE == 11:
            EVENT = DATA['t']
            print(f'[ {EVENT} ]')
            print(DATA)

        else:
            print(DATA)



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

                listener = Receiver(
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

