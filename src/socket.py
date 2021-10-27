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

    __BASE  = 'https://discord.com/api/v9'

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
        self.__seq = 0
        self.__ws = None
        self.__raw = None
        self.__uri = None
        self.ping = 0
        self.__ack_time = 0
        self.__frequency = 0
        self.__start_time = 0
        self.__session = None
        self.__session_id = None
        self.raw_received = None

        # starters
        self.prefix = prefix
        self.__secret = secret
        self.app_id = app_id
        self.intents = intents
        self.commands = commands
        self.guild_id = guild_id
        self.slash_cmds = slash_cmds


    async def __get_gateway(self):
        URL = "https://discordapp.com/api/gateway"
        response = await self.__session.get(URL)
        js = await response.json()
        return js['url']

    async def __keep_alive(self):
        data = self.__raw
        if data['op'] == 10:
            self.__frequency = data['d']['heartbeat_interval'] / 1000
            asyncio.ensure_future(
                self.__heartbeat_send()
            )

    async def __heartbeat_ack(self):
        data = self.__raw
        if data['op'] == 11:
            self.__ack_time = time.time() * 1000
            ping_time = self.__ack_time - self.__start_time
            self.ping = ping_time
            print(f'[ PING {round(ping_time)}MS ]')

    async def __heartbeat_send(self):
        while True:
            await asyncio.sleep(self.__frequency)
            self.__start_time = time.time() * 1000
            await self.__ws.send_json({"op": 1, "d": None})

    async def __update_ssn(self):
        raw = self.__raw
        if raw['op'] == 0 and raw['t'] == 'READY':
            self.__session_id = raw['d']['session_id']
            print(f'[ SESSION ID: {self.__session_id} ]')

    async def __identify(self):
        raw = self.__raw
        if raw['op'] == 10:
            await self.__ws.send_json(
                {
                    "op": 2,
                    "d": {
                        "token": self.__secret,
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

    async def __update_seq(self):
        seq = self.__raw['s']
        if seq:
            self.__seq = seq

    async def __start_listener(self):
        async with self.__session.ws_connect(
                f"{self.__uri}?v=9&encoding=json") as ws:

            async for msg in ws:
                self.__ws = ws
                raw = json.loads(msg.data)
                self.__raw = raw

                await self.__identify()
                await self.__req_members()
                await self.__reconnect()
                await self.__update_ssn()
                await self.__update_seq()

                await EventManager(
                    socket = self.__ws,
                    raw_response = raw,
                    add_id = self.app_id,
                    prefix = self.prefix,
                    secret = self.__secret,
                    session = self.__session,
                    intents = self.intents,
                    c_bucket = self.commands,

                ).run()

                await self.__keep_alive()
                await self.__heartbeat_ack()

    async def connect(self):
        async with aiohttp.ClientSession() as session:
            self.__session = session
            self.__uri = await self.__get_gateway()
            await self.__slash_register()
            await self.__start_listener()

    async def __reconnect(self):
        if self.__raw['op'] == 7:
            await self.__ws.send_json(
                {
                    "op": 6,
                    "d": {
                        "token": self.__secret,
                        "session_id": self.__session_id,
                        "seq": self.__seq
                    }
                }
            )

    async def __slash_register(self):
        if self.guild_id and self.app_id:
            for item in self.slash_cmds:
                resp = await self.__session.post(
                    f'{self.__BASE}/applications/{self.app_id}'
                    f'/guilds/{self.guild_id}/commands',
                    json = await item.__call__(),
                    headers = {"Authorization": f"Bot {self.__secret}"}
                )
                js = await resp.json()
                await Stack(js).slash()
            print("[ SLASH REGD ]")
        else:
            raise ValueError(
                "Application Id and Test Guild Id is mandatory to register slash command"
            )

    async def __req_members(self):
        raw = self.__raw
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
                await self.__ws.send_json(payload)

