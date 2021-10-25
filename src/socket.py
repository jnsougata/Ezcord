import json
import time
import asyncio
import aiohttp
from src.map import Map
from src.cmd import Executor
from src.stacking import Stack
from src.slash import _ParseSlash


class EventManager:

    def __init__(
            self,
            secret: str,
            response: dict,
            bucket: list,
            prefix: str,
            intents: int,
            session: aiohttp.ClientSession,
            socket: aiohttp.ClientWebSocketResponse,
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
            print(f'[ {EVENT} ] [ SEQ {DATA["s"]} ]')

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
                slash = _ParseSlash(RAW)
                await slash.callback(self.session)

            elif EVENT == 'MESSAGE_CREATE':
                ctx = Map(
                    payload= RAW,
                    session = self.session,
                    secret = self.secret
                )

                parse = Executor(
                    ctx = ctx,
                    prefix = self.prefix,
                    bucket = self.bucket,
                )
                await parse.process_message

            else:
                print(f'[ {EVENT} ]\n{DATA}')


        # RECEIVED HELLO
        elif CODE == 10:

            #CACHING HELLO
            await Stack(DATA).hello()

        # HEART BEAT ACK
        elif CODE == 11:
            pass

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
        self.seq = 0
        self.latency = 0
        self.ack_time = 0
        self.frequency = 0
        self.start_time = 0

        self.ws = None
        self.raw = None
        self.session = None
        self.secret = secret
        self.bucket = bucket
        self.prefix = prefix
        self.session_id = None
        self.intents = intents



    async def get_gateway_url(self):
        URL = "https://discordapp.com/api/gateway"
        response = await self.session.get(URL)
        js = await response.json()
        return js['url']


    async def keep_alive(self):
        data = self.raw
        if data['op'] == 10:
            self.frequency = data['d']['heartbeat_interval'] / 1000
            asyncio.ensure_future(
                self.heartbeat_send()
            )


    async def heartbeat_ack(self):
        data = self.raw
        if data['op'] == 11:
            self.ack_time = time.time() * 1000
            ping_time = self.ack_time - self.start_time
            self.latency = ping_time
            print(f'[ PING {round(ping_time)}MS ]')

    async def heartbeat_send(self):
        while True:
            await asyncio.sleep(self.frequency)
            self.start_time = time.time() * 1000
            await self.ws.send_json(
                {
                    "op": 1,
                    "d": None
                }
            )

    async def set_session_id(self):
        raw = self.raw
        if raw['op'] == 0 and raw['t'] == 'READY':
            self.session_id = raw['d']['session_id']
            print(f'[ SESSION ID: {self.session_id} ]')

    async def identify(self):
        raw = self.raw
        if raw['op'] == 10:
            await self.ws.send_json(
                {
                    "op": 2,
                    "d": {
                        "token": self.secret,
                        "intents": self.intents,
                        "properties": {
                            '$os': "ios",
                            '$browser': 'Discord iOS',
                            '$device': 'Easycord',
                            '$referrer': '',
                            '$referring_domain': ''
                        }
                    }
                }
            )

    async def update_sequence(self):
        seq = self.raw['s']
        if seq:
            self.seq = seq

    async def gateway_listener(self, url: str):
        async with self.session.ws_connect(
                f"{url}?v=9&encoding=json") as ws:

            async for msg in ws:
                self.ws = ws
                raw = json.loads(msg.data)
                self.raw = raw

                await self.set_session_id()
                await self.identify()
                await self.update_sequence()
                await self.reconnect()

                insp = EventManager(
                    response = raw,
                    socket = self.ws,
                    secret = self.secret,
                    session = self.session,
                    bucket = self.bucket,
                    prefix = self.prefix,
                    intents = self.intents
                )
                await insp.run()

                await self.keep_alive()
                await self.heartbeat_ack()


    async def connect(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            uri = await self.get_gateway_url()
            await self.gateway_listener(uri)

    async def reconnect(self):
        if self.raw['op'] == 7:
            await self.ws.send_json(
                {
                    "op": 6,
                    "d": {
                        "token": self.secret,
                        "session_id": self.session_id,
                        "seq": self.seq
                    }
                }
            )



