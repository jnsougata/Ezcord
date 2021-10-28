import json
import time
import asyncio
import aiohttp
from src.cmd import Executor
from src.context import Context
from src.slash_ import _ParseSlash



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
        self.__ping = 0
        self.__ack_time = 0
        self.__start_time = 0
        self.__session = None
        self.__session_id = None

        # caching
        self.users = {}
        self.__guilds = {}
        self.__hello = None
        self.__ready = None
        self.__slash_data = {}

        # starters
        self.prefix = prefix
        self.app_id = app_id
        self.__secret = secret
        self.intents = intents
        self.commands = commands
        self.guild_id = guild_id
        self.__slash_cmds = slash_cmds


    async def __get_gateway(self):
        URL = "https://discordapp.com/api/gateway"
        response = await self.__session.get(URL)
        js = await response.json()
        return js['url']

    async def __keep_alive(self):
        if self.__raw['op'] == 10:
            data = self.__hello
            sleep = data['heartbeat_interval'] / 1000
            asyncio.ensure_future(
                self.__heartbeat_send(sleep)
            )

    async def __heartbeat_ack(self):
        data = self.__raw
        if data['op'] == 11:
            self.__ack_time = time.time() * 1000
            ping_time = self.__ack_time - self.__start_time
            print(f'[ PING {round(ping_time)}MS ]')

    async def __heartbeat_send(self, interval):
        while True:
            await asyncio.sleep(interval)
            self.__start_time = time.time() * 1000
            await self.__ws.send_json({"op": 1, "d": None})

    async def __update_ssn(self):
        raw = self.__raw
        if raw['op'] == 0 and raw['t'] == 'READY':
            self.__session_id = raw['d']['session_id']
            print(f'[ SESSION ID UPDATED]')

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

                await self.__cache_hello()
                await self.__keep_alive()
                await self.__cache_ready()
                await self.__identify()
                await self.__cache_guild()
                await self.__req_members()
                await self.__cache_members()
                await self.__update_ssn()
                await self.__update_seq()
                await self.__heartbeat_ack()
                await self.__reconnect()

                if raw['t'] == 'MESSAGE_CREATE':
                    ctx = Context(
                        payload=raw['d'],
                        session=self.__session,
                        secret=self.__secret,
                        guildcache=self.__guilds
                    )

                    parse = Executor(
                        ctx=ctx,
                        prefix=self.prefix,
                        bucket=self.commands,
                    )
                    await parse.process_message


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
            for item in self.__slash_cmds:
                resp = await self.__session.post(
                    f'{self.__BASE}/applications/{self.app_id}'
                    f'/guilds/{self.guild_id}/commands',
                    json = await item.__call__(),
                    headers = {"Authorization": f"Bot {self.__secret}"}
                )
                js = await resp.json()
                CMD_ID = js['id']
                self.__slash_data[str(CMD_ID)] = js
            print("[ SLASH REGD ]")

        else:
            raise ValueError(
                "Application Id and Test Guild Id is mandatory to register slash command"
            )

    async def __req_members(self):
        raw = self.__raw
        if raw['t'] == 'GUILD_CREATE':
            payload = {
                "op": 8,
                "d": {
                    "guild_id": int(raw['d']['id']),
                    "query": "",
                    "limit": 0
                }
            }
            await self.__ws.send_json(payload)

    # caching functions
    async def __cache_hello(self):
        if self.__raw['op'] == 10:
            self.__hello = self.__raw['d']
            print('[ CACHING HELLO ]')

    async def __cache_ready(self):
        if self.__raw['t'] == 'READY':
            self.__ready = self.__raw['d']
            print('[ CACHING READY ]')

    async def __cache_guild(self):
        data = self.__raw
        if data['t'] == 'GUILD_CREATE':
            guild_id = data['d']['id']
            self.__guilds[str(guild_id)] = data['d']
            print(f'[ CACHING GUILD {guild_id} ]')

    async def __cache_members(self):
        data = self.__raw
        if data['t'] == 'GUILD_MEMBERS_CHUNK':
            guild_id = data['d']['guild_id']
            temp = dict()
            for member in data['d']['members']:
                user_id = member['user']['id']
                temp[str(user_id)] = member
            self.__guilds[str(guild_id)]['members'] = temp
            print(f'[ CACHING MEMBER FOR GUILD {guild_id} ]')

