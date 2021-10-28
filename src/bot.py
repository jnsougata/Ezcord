import asyncio
import aiohttp
from functools import wraps
from src.slash import Slash
from src.socket import Websocket


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
        self.__slash_cmds = []
        self.__normal_commands = []


        super().__init__(
            secret=token,
            app_id=app_id,
            prefix=prefix,
            intents=intents,
            guild_id=guild_id,
            slash_cmds=self.__slash_cmds,
            commands=self.__normal_commands
        )

    def slash_command(self, command: Slash):
        self.__slash_cmds.append(command.json)
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func
            self.__normal_commands.append(wrapper())
        return decorator



    def command(self, fn):
        self.__normal_commands.append(fn)


    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.connect())



