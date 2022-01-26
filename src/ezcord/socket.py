import os
import sys
import json
import time
import asyncio
import aiohttp
import traceback
from .user import User
from .member import Member
from .context import Context
from .message import Message
from .slash import SlashContext
from .executor import CommandExecutor, SlashExecutor

intro = '''
 _____   _____           ____    ___    ____    ____  
| ____| |__  /          / ___|  / _ \  |  _ \  |  _ \ 
|  _|     / /   _____  | |     | | | | | |_) | | | | |
| |___   / /_  |_____| | |___  | |_| | |  _ <  | |_| |
|_____| /____|          \____|  \___/  |_| \_\ |____/
....................................................
'''


class WebSocket:

    def __init__(
            self,
            prefix: str,
            app_id: int,
            token: str,
            intents: int,
            guild_id: int,
            events: dict,
            commands: dict,
            slash_queue: list,
    ):
        # runtime
        self._seq = 0
        self._ack = 0
        self._sent = 0
        self.latency = 0
        self._ws = None
        self._uri = None
        self._raw = None
        self.http = None
        self._interval = None
        self._session = None
        self._prefix = prefix
        self._app_id = app_id
        self._secret = token
        self._events = events
        self._intents = intents
        self._commands = commands
        self._test_guild = guild_id
        self._reg_queue = slash_queue

        # main cache
        self.__cached = {'ready': None, 'hello': None, 'users': {}, 'guilds': {}, 'channels': {}}

    async def _get_gateway(self):
        url = "https://discordapp.com/api/gateway"
        resp = await self._session.get(url)
        gateway = await resp.json()
        return gateway.get('url')

    async def _keep_alive(self):
        if self._raw['op'] == 10:
            asyncio.ensure_future(self._heartbeat_send(self._interval / 1000))

        if self._raw['op'] == 11:
            self._ack = time.perf_counter() * 1000
            self.latency = round(self._ack - self._sent)

    async def _heartbeat_send(self, duration: float):
        while True:
            self._sent = time.perf_counter() * 1000
            await self._ws.send_json({"op": 1, "d": None})
            await asyncio.sleep(duration)

    async def _store_session(self):
        raw = self._raw
        if raw['op'] == 0 and raw['t'] == 'READY':
            self._session_id = raw['d']['session_id']

    async def _identify(self):
        raw = self._raw
        if raw['op'] == 10:
            await self._ws.send_json(
                {
                    "op": 2,
                    "d": {
                        "token": self._secret,
                        "intents": self._intents,
                        "properties": {
                            '$os': "linux",
                            '$browser': 'discord',
                            '$device': 'discord',
                        }
                    }
                }
            )

    async def _update_sequence(self):
        seq = self._raw['s']
        if seq:
            self._seq = seq

    async def __start_listener(self):
        async with self._session.ws_connect(f"{self._uri}?v=9&encoding=json") as ws:
            async for msg in ws:
                self._ws = ws
                raw = json.loads(msg.data)
                self._raw = raw
                task = asyncio.create_task(self._cache_ready())
                done, _ = await asyncio.wait({task})
                if task in done:
                    await self._event_listener_pool()
                    await self._cache_hello()
                    await self._keep_alive()
                    await self._identify()
                    await self._cache_guild()
                    await self._req_members()
                    await self._cache_members()
                    await self._store_session()
                    await self._update_sequence()
                    await self._reconnect()
                    await self._command_executor()

    async def _connect(self):
        print(intro)
        async with aiohttp.ClientSession() as session:
            self._session = session
            self.__cached['session'] = session
            self._uri = await self._get_gateway()
            await self._reg_slash()
            await self.__start_listener()

    async def _reconnect(self):
        if self._raw['op'] == 7:
            await self._ws.send_json(
                {
                    "op": 6,
                    "d": {
                        "token": self._secret,
                        "session_id": self._session_id,
                        "seq": self._seq
                    }
                }
            )

    async def _reg_slash(self):
        if self._reg_queue:
            print('[🗗] Registering Slash Commands')
            for item in self._reg_queue:
                resp = await self._session.post(
                    f'https://discord.com/api/v9/applications/{self._app_id}/guilds/{self._test_guild}/commands',
                    json=item,
                    headers={"Authorization": f"Bot {self._secret}"}
                )
                if resp.status == 200:
                    print(f"[✓] CMD: {item['name']}")
                else:
                    print(f"[x] CMD: {item['name']}")

    async def _command_executor(self):
        if self._raw['t'] == 'MESSAGE_CREATE':
            payload = self._raw['d']
            payload['_token'] = self._secret
            payload['session'] = self._session
            _ctx = Context(payload, self.__cached)
            await CommandExecutor(_ctx, self._prefix, self._commands).process()
        if self._raw['t'] == 'INTERACTION_CREATE':
            pass

    #  initialize cache
    async def _req_members(self):
        raw = self._raw
        if raw['t'] == 'GUILD_CREATE':
            payload = {
                "op": 8,
                "d": {
                    "guild_id": int(raw['d']['id']),
                    "query": "",
                    "limit": 0
                }
            }
            await self._ws.send_json(payload)

    async def _cache_hello(self):
        if self._raw['op'] == 10:
            self.__cached['hello'] = self._raw['d']
            self._interval = self._raw['d']['heartbeat_interval']

    async def _cache_ready(self):
        if self._raw['t'] == 'READY':
            self.__cached['ready'] = self._raw['d']

    async def _cache_guild(self):
        data = self._raw
        if data['t'] == 'GUILD_CREATE':
            guild_data = data['d']
            guild_id = str(data['d']['id'])
            bulk_channel_data = {}
            bulk_role_data = {}
            # hashing channels for faster lookup
            for channel in guild_data['channels']:
                channel_id = str(channel['id'])
                channel_data = channel
                bulk_channel_data[channel_id] = channel_data
                self.__cached['channels'][channel_id] = channel_data
            data['d']['channels'] = bulk_channel_data
            # hashing roles for faster lookup
            for role in guild_data['roles']:
                role_id = str(role['id'])
                role_data = role
                bulk_role_data[role_id] = role_data
            guild_data['roles'] = bulk_role_data
            # hashing guilds for faster lookup
            self.__cached['guilds'][guild_id] = guild_data

    async def _cache_members(self):
        data = self._raw
        if data['t'] == 'GUILD_MEMBERS_CHUNK':
            guild_id = str(data['d']['guild_id'])
            bulk_member_data = {}
            # hashing users for faster lookup
            for member in data['d']['members']:
                member['guild_id'] = guild_id
                member_data = member
                user_data = member['user']
                user_id = str(user_data['id'])
                self.__cached['users'][user_id] = user_data
                bulk_member_data[user_id] = member_data
            # hashing members for faster lookup
            self.__cached['guilds'][guild_id]['members'] = bulk_member_data

    # direct methods
    @property
    def user(self):
        self_data = self.__cached['ready']['user']
        return User(self_data)

    def get_user(self, user_id: int):
        return self.__cached['users'][str(user_id)]

    def get_guild(self, guild_id: int):
        return self.__cached['guilds'][str(guild_id)]

    def get_channel(self, channel_id: int):
        return self.__cached['channels'][str(channel_id)]

    # listener events -----------------------
    async def _event_listener_pool(self):
        await self._ready_listener()
        await self._message_create_listener()

    async def _ready_listener(self):
        if self._raw['t'] == 'READY':
            ready_event = self._events.get('on_ready')
            if ready_event:
                try:
                    await ready_event()
                except Exception:
                    traceback.print_exception(*sys.exc_info())

    async def _message_create_listener(self):
        if self._raw['t'] == 'MESSAGE_CREATE':
            msg_event = self._events.get('on_message')
            data = self._raw['d']
            data['_token'] = self._secret
            data['session'] = self._session
            if msg_event:
                try:
                    await msg_event(Message(data))
                except Exception:
                    traceback.print_exception(*sys.exc_info())
