import json
import time
import asyncio
import aiohttp
from src.ez.map import Map
from src.ez.cmd import Executor
from src.ez.stacking import Stack
from src.ez.slash import SlashReply


class Receiver:

    def __init__(
            self,
            secret: str,
            response: dict,
            session: aiohttp.ClientSession,
            socket: aiohttp.ClientWebSocketResponse,
            bucket: list,
            prefix: str,
            intents: int,
    ):
        self.ws = socket
        self.ack_time = 0
        self.start_time = 0
        self.secret = secret
        self.bucket = bucket
        self.prefix = prefix
        self.data = response
        self.session = session
        self.auth_header = {
            "Authorization": f"Bot {secret}"
        }
        self.intents = intents


    @property
    async def op(self):
        return int(self.data['op'])


    async def send_(self, content:str, channel_id: int):
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
            RAW = DATA['d']
            cache = Stack(DATA)
            print(f'[ {EVENT} ]')

            # CHECKING EVENT TYPE
            if EVENT == 'READY':
                await cache.ready()

            elif EVENT == 'GUILD_CREATE':
                await cache.guild()
                await Stack.members(
                    auth_header = self.auth_header,
                    guild_id = DATA['d']['id'],
                    session = self.session
                )

            elif EVENT == 'INTERACTION_CREATE':
                slash = SlashReply(RAW)
                await slash.callback(self.session)

            elif EVENT == 'MESSAGE_CREATE':
                ctx = Map(
                    response = RAW,
                    session = self.session,
                    secret = self.secret
                )

                PARSER = Executor(
                    ctx = ctx,
                    prefix = self.prefix,
                    bucket = self.bucket,
                )
                await PARSER.process_message

            else:
                print(f'[ {EVENT} ]\n{DATA}')


        # RECEIVED HELLO
        elif CODE == 10:
            await Stack(DATA).hello()

            # SENDING IDENTIFICATION PAYLOAD
            await self.ws.send_json(
                {
                    "op": 2,
                    "d": {
                        "token": self.secret,
                        "intents": self.intents,
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
            print(f'[ HEARTBEAT ACK ]')

        else:
            print(DATA)



class Websocket:
    def __init__(
            self,
            secret: str,
            prefix:str,
            bucket: list,
            intents: int
    ):
        self.ws = None
        self.session = None
        self.secret = secret
        self.start_time = 0
        self.ack_time = 0
        self.interval = 0
        self.bucket = bucket
        self.prefix = prefix
        self.intents = intents



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
            await Stack.latency(self.ack_time - self.start_time)


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
                    bucket = self.bucket,
                    prefix = self.prefix,
                    intents = self.intents
                )
                await listener.run()
                await self.send_heartbeat(data)
                await self.heartbeat_ack(data)


    async def connect(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            gateway = await self.getGateway()
            await self.handler(gateway)

