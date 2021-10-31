import asyncio
import aiohttp
from .slash import Slash
from .guild import Guild
from .channel import Channel
from functools import wraps
from .socket import WebSocket


class Bot(WebSocket):
    def __init__(
            self,
            token: str,
            prefix: str,
            intents: int,
            app_id: int = None,
            guild_id: int = None,
    ):
        self._events = []
        self._cmd_pool = []
        self._slash_queue = []
        self._app_id = app_id
        self.prefix = prefix
        self._secret = token
        self.intents = intents
        self.guild_id = guild_id


        super().__init__(
            secret=token,
            app_id=app_id,
            prefix=prefix,
            intents=intents,
            guild_id=guild_id,
            events = self._events,
            commands = self._cmd_pool,
            slash_queue= self._slash_queue,
        )

    @property
    def id(self):
        return self._ready['user']['id']

    @property
    def avatar(self):  # to object
        return self._ready['user']['avatar']

    @property
    def name(self):
        return self._ready['user']['username']

    @property
    def discriminator(self):
        return self._ready['user']['discriminator']

    @property
    def guilds(self):
        return len(self._guilds)

    @property
    def channels(self):
        return len(self._channels)


    def pull_guild(self, id: int):
        return Guild(
            Id=id,
            secret=self._secret,
            payload=self._guilds,
            session=self._session,
        )

    def pull_channel(self, id: int):
        return Channel(
            secret=self._secret,
            payload=self._channels[str(id)],
            session=self._session,
        )






    def slash_cmd(self, command: Slash):
        self._slash_queue.append(command.json)
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func
            self._cmd_pool.append(wrapper())
        return decorator



    def cmd(self, fn):
        self._cmd_pool.append(fn)



    def listen(self, fn):
        self._events.append(fn)


    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._connect())



