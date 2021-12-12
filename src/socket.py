import os
import sys
import json
import time
import asyncio
import aiohttp
import traceback
from .cprint import Log
from .member import Member
from .context import Context
from .message import Message
from .slash import SlashContext
from .exe import MsgExec, SlasExec


class WebSocket:
    __head = 'https://discord.com/api/v9'

    def __init__(
            self,
            prefix: str,
            app_id: int,
            secret: str,
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
        self._session = None
        self._session_id = None
        self._users = {}
        self._guilds = {}
        self._channels = {}
        self._hello = None
        self._ready = None
        self._prefix = prefix
        self._app_id = app_id
        self._secret = secret
        self._events = events
        self._intents = intents
        self._commands = commands
        self._test_guild = guild_id
        self._reg_queue = slash_queue

    async def _get_gateway(self):
        URL = "https://discordapp.com/api/gateway"
        response = await self._session.get(URL)
        _json = await response.json()
        return _json['url']

    async def _keep_alive(self):
        if self._raw['op'] == 10:
            data = self._hello
            sleep = data['heartbeat_interval'] / 1000
            asyncio.ensure_future(
                self._heartbeat_send(sleep)
            )

    async def _heartbeat_ack(self):
        data = self._raw
        if data['op'] == 11:
            self._ack = time.perf_counter() * 1000
            self.latency = round(self._ack - self._sent)

    async def _heartbeat_send(self, dur):
        while True:
            self._sent = time.perf_counter() * 1000
            await self._ws.send_json({"op": 1, "d": None})
            await asyncio.sleep(dur)

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

    async def _update_seq(self):
        seq = self._raw['s']
        if seq:
            self._seq = seq

    async def __start_listener(self):
        async with self._session.ws_connect(
                f"{self._uri}?v=9&encoding=json") as ws:
            async for msg in ws:
                self._ws = ws
                raw = json.loads(msg.data)
                self._raw = raw
                await self._event_pool()
                await self._cache_hello()
                await self._keep_alive()
                await self._cache_ready()
                await self._identify()
                await self._cache_guild()
                await self._req_members()
                await self._cache_members()
                await self._store_session()
                await self._update_seq()
                await self._heartbeat_ack()
                await self._reconnect()
                await self._cmd_checker(raw)

    async def _connect(self):
        Log.purple('''
 _____   _____           ____    ___    ____    ____  
| ____| |__  /          / ___|  / _ \  |  _ \  |  _ \ 
|  _|     / /   _____  | |     | | | | | |_) | | | | |
| |___   / /_  |_____| | |___  | |_| | |  _ <  | |_| |
|_____| /____|          \____|  \___/  |_| \_\ |____/
    ''')
        Log.green(f'[🔌] 🖿 ━━━━━━━━━ ✓ ━━━━━━━━━ 🌐')
        async with aiohttp.ClientSession() as session:
            self._session = session
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
            Log.purple('[🗗] Registering Slash Commands')
            for item in self._reg_queue:
                resp = await self._session.post(
                    f'{self.__head}/applications/{self._app_id}'
                    f'/guilds/{self._test_guild}/commands',
                    json=item,
                    headers={"Authorization": f"Bot {self._secret}"}
                )
                if resp.status == 200:
                    Log.green(f"[✓] CMD: {item['name']}")
                else:
                    Log.red(f"[x] CMD: {item['name']}")

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

    async def _on_ready(self):
        raw = self._raw
        if raw['t'] == 'READY':
            Log.blurple('[▶] Processing Internal Cache')
            ready_event = self._events.get('on_ready')
            if ready_event:
                try:
                    await ready_event()
                except Exception:
                    traceback.print_exception(*sys.exc_info())

    async def _on_message(self):
        raw = self._raw
        if raw['t'] == 'MESSAGE_CREATE':
            msg_event = self._events.get('on_message')
            if msg_event:
                try:
                    await msg_event(
                        Message(
                            payload=raw['d'],
                            guild_cache=self._guilds,
                            session=self._session,
                            secret=self._secret
                        )
                    )
                except Exception:
                    traceback.print_exception(*sys.exc_info())

    async def _on_member_update(self):
        raw = self._raw
        if raw['t'] == 'GUILD_MEMBER_UPDATE':
            try:
                with open('src/cache.json', 'w') as f:
                    json.dump(self._guilds, f)
                guild_id = raw['d']['guild_id']
                user_id = raw['d']['user']['id']
                old_guilds = self._guilds
                members = old_guilds[str(guild_id)]['members']
                for key, value in raw['d'].items():
                    members[str(user_id)][key] = value
                self._guilds[str(guild_id)]['members'] = members
                old = Member(
                    secret=self._secret,
                    user_id=int(user_id),
                    session=self._session,
                    guild_id=int(guild_id),
                    guild_cache=json.load(open('src/cache.json')),
                )
                new = Member(
                    secret=self._secret,
                    user_id=int(user_id),
                    session=self._session,
                    guild_id=int(guild_id),
                    guild_cache=self._guilds,
                )
                func = self._events.get('on_member_update')
                if func:
                    await func(old, new)
            except Exception:
                traceback.print_exception(*sys.exc_info())

    async def _event_pool(self):
        await self._on_ready()
        await self._on_message()
        await self._on_member_update()

    async def _cmd_checker(self, raw: dict):
        if raw['t'] == 'MESSAGE_CREATE':
            ctx = Context(
                payload=raw['d'],
                session=self._session,
                secret=self._secret,
                guildcache=self._guilds
            )
            await MsgExec(
                ctx=ctx,
                prefix=self._prefix,
                bucket=self._commands,
            ).process_message()

        if raw['t'] == 'INTERACTION_CREATE':
            slash_ctx = SlashContext(
                response=raw['d'],
                session=self._session,
                bot_token=self._secret,
                guild_cache=self._guilds
            )
            await SlasExec(
                ctx=slash_ctx,
                bucket=self._commands
            ).process_slash()

    async def _cache_hello(self):
        if self._raw['op'] == 10:
            self._hello = self._raw['d']

    async def _cache_ready(self):
        if self._raw['t'] == 'READY':
            data = self._raw['d']
            temp = dict()
            temp[data['user']['id']] = {'user': data['user']}
            data['user'] = temp
            self._ready = data

    async def _cache_guild(self):
        data = self._raw
        if data['t'] == 'GUILD_CREATE':
            guild_id = data['d']['id']
            ch_cache = dict()
            for channel in data['d']['channels']:
                ch_cache[str(channel['id'])] = channel
                self._channels[str(channel['id'])] = channel
            data['d']['channels'] = ch_cache
            role_cache = dict()
            for role in data['d']['roles']:
                role_cache[str(role['id'])] = role
            data['d']['roles'] = role_cache
            self._guilds[str(guild_id)] = data['d']

    async def _cache_members(self):
        data = self._raw
        if data['t'] == 'GUILD_MEMBERS_CHUNK':
            guild_id = data['d']['guild_id']
            cache = dict()
            for user in data['d']['members']:
                user_id = user['user']['id']
                cache[str(user_id)] = user
                self._users[str(user_id)] = user
            self._guilds[str(guild_id)]['members'] = cache
