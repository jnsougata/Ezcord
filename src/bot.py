import asyncio
import aiohttp
from .slash import Slash
from functools import wraps
from .socket import Websocket


class Bot(Websocket):
    def __init__(
            self,
            token: str,
            prefix: str,
            intents: int,
            app_id: int = None,
            guild_id: int = None,
    ):

        self.app_id = app_id
        self.prefix = prefix
        self.__secret = token
        self.intents = intents
        self.guild_id = guild_id
        self.__events = []
        self.__cmd_funcs = []
        self.__slash_reg = []



        super().__init__(
            secret=token,
            app_id=app_id,
            prefix=prefix,
            intents=intents,
            guild_id=guild_id,
            events = self.__events,
            commands = self.__cmd_funcs,
            slash_cmds = self.__slash_reg,
        )

    def slash_command(self, command: Slash):
        self.__slash_reg.append(command.json)
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func
            self.__cmd_funcs.append(wrapper())
        return decorator



    def command(self, fn):
        self.__cmd_funcs.append(fn)



    def event(self, fn):
        self.__events.append(fn)


    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.connect())



