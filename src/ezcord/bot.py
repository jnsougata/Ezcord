import os
import asyncio
import aiohttp
from .user import User
from .cprint import Log
from .slash import Slash
from .guild import Guild
from functools import wraps
from .channel import Channel
from .socket import WebSocket


class Bot(WebSocket):
    def __init__(
            self,
            prefix: str,
            intents: int,
            app_id: int = None,
            guild_id: int = None,
    ):
        self._events = {}
        self._cmd_pool = {}
        self._slash_queue = []
        self._app_id = app_id
        self.prefix = prefix
        self._secret = ''
        self.intents = intents
        self.guild_id = guild_id
        super().__init__(
            app_id=app_id,
            prefix=prefix,
            intents=intents,
            guild_id=guild_id,
            events=self._events,
            token=self._secret,
            commands=self._cmd_pool,
            slash_queue=self._slash_queue,
        )

    @property
    def guilds(self):
        return len(self._guilds)

    @property
    def channels(self):
        return len(self._channels)

    def slash_command(self, command: Slash):
        self._slash_queue.append(command.json)

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func

            self._cmd_pool[command.json["name"]] = wrapper()

        return decorator

    def command(self, name: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func

            self._cmd_pool[name] = wrapper()

        return decorator

    def event(self, fn):
        self._events[fn.__name__] = fn

    def run(self, token: str):
        self._secret = token
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self._connect())
        except KeyboardInterrupt:
            Log.purple('[!] --------------------------')
            Log.red(f'[🔌] 🖿 ━━━━━━━━━ x ━━━━━━━━━ 🌐')
            os._exit(0)
