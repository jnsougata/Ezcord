import asyncio
import aiohttp
from functools import wraps
from src.slash_ import Slash
from src.stacking import Stack
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
        self.secret = token
        self.app_id = app_id
        self.prefix = prefix
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


    def slash_command(self, fn):
        self.__slash_cmds.append(fn)

    def command(self, fn):
        self.__normal_commands.append(fn)


    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.connect())



