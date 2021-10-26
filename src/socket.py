import json
import time
import asyncio
import aiohttp
from src.context import Context
from src.cmd import Executor
from src.stacking import Stack
from src.slash_ import _ParseSlash


class EventManager:

    BASE = base = 'https://discord.com/api/v9'

    def __init__(
            self,
            secret: str,
            prefix: str,
            intents: int,
            add_id: int,
            c_bucket: list,
            raw_response: dict,
            session: aiohttp.ClientSession,
            socket: aiohttp.ClientWebSocketResponse,
    ):
        self.ws = socket
        self.ack_time = 0
        self.start_time = 0
        self.secret = secret
        self.cmds = c_bucket
        self.app_id = add_id
        self.prefix = prefix
        self.session = session
        self.intents = intents
        self.data = raw_response
        self.auth_header = {
            "Authorization": f"Bot {secret}"
        }



    @property
    async def op(self):
        return int(self.data['op'])


    async def send(self, content:str, channel_id: int):
        await self.session.post(
            f'{self.BASE}/channels/{channel_id}/messages',
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

            elif EVENT == 'INTERACTION_CREATE':
                slash = _ParseSlash(RAW)
                await slash.callback(self.session)

            elif EVENT == 'MESSAGE_CREATE':
                ctx = Context(
                    payload= RAW,
                    session = self.session,
                    secret = self.secret
                )

                parse = Executor(
                    ctx = ctx,
                    prefix = self.prefix,
                    bucket = self.cmds,
                )
                await parse.process_message

            elif EVENT == 'GUILD_MEMBERS_CHUNK':
                await cache.members()
                print(list(DATA['d']))

            else:
                print(DATA)


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

    BASE = base = 'https://discord.com/api/v9'

    def __init__(
            self,
            prefix:str,
            app_id: int,
            secret: str,
            intents: int,
            guild_id: int,
            commands: list,
            slash_cmds: list,
    ):
        # runtime
        self.seq = 0
        self.ws = None
        self.raw = None
        self.uri = None
        self.ping = 0
        self.ack_time = 0
        self.frequency = 0
        self.start_time = 0
        self.session = None
        self.session_id = None
        self.raw_received = None

        # starters
        self.prefix = prefix
        self.secret = secret
        self.app_id = app_id
        self.intents = intents
        self.commands = commands
        self.guild_id = guild_id
        self.slash_cmds = slash_cmds


    async def get_gateway(self):
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
            self.ping = ping_time
            print(f'[ PING {round(ping_time)}MS ]')

    async def heartbeat_send(self):
        while True:
            await asyncio.sleep(self.frequency)
            self.start_time = time.time() * 1000
            await self.ws.send_json({"op": 1, "d": None})

    async def update_ssn(self):
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

    async def update_seq(self):
        seq = self.raw['s']
        if seq:
            self.seq = seq

    async def start_listener(self):
        async with self.session.ws_connect(
                f"{self.uri}?v=9&encoding=json") as ws:

            async for msg in ws:
                self.ws = ws
                raw = json.loads(msg.data)
                self.raw = raw

                await self.identify()
                await self.req_members()
                await self.reconnect()
                await self.update_ssn()
                await self.update_seq()

                await EventManager(
                    socket = self.ws,
                    raw_response = raw,
                    add_id = self.app_id,
                    prefix = self.prefix,
                    secret = self.secret,
                    session = self.session,
                    intents = self.intents,
                    c_bucket = self.commands,

                ).run()

                await self.keep_alive()
                await self.heartbeat_ack()

    async def connect(self):
        async with aiohttp.ClientSession() as session:
            self.session = session
            self.uri = await self.get_gateway()
            await self.slash_register()
            await self.start_listener()

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

    async def slash_register(self):
        if self.guild_id and self.app_id:
            for item in self.slash_cmds:
                resp = await self.session.post(
                    f'{self.BASE}/applications/{self.app_id}'
                    f'/guilds/{self.guild_id}/commands',
                    json = await item.__call__(),
                    headers = {"Authorization": f"Bot {self.secret}"}
                )
                js = await resp.json()
                await Stack(js).slash()
            print("[ SLASH REGD ]")
        else:
            raise ValueError(
                "Application Id and Test Guild Id is mandatory to register slash command"
            )

    async def req_members(self):
        raw = self.raw
        if raw['op'] == 10:

            rs = json.load(open("src/stack/ready_stack.json", "r"))
            guilds = [item['id'] for item in rs['d']['guilds']]
            for item in guilds:
                payload = {
                    "op": 8,
                    "d": {
                        "guild_id": item,
                        "query": "",
                        "limit": 0
                    }
                }
                await self.ws.send_json(payload)

