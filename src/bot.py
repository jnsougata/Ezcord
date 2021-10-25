import asyncio
import aiohttp

from src.stacking import Stack
from src.slash import MakeSlash
from src.socket import Websocket



class Bot:
    def __init__(
            self,
            token: str,
            prefix: str,
            commands: list,
            intents: int,
            app_id: int = None,
            guild_id: int = None,
            slash_commands: list[MakeSlash] = None,

    ):

        self.secret = token
        self.app_id = app_id
        self.prefix = prefix
        self.bucket = commands
        self.guild_id = guild_id
        self.slash = slash_commands
        self.slash_auth = {
            "Authorization": f"Bot {token}",
            "content-type": "application/json"
        }
        self.intents = intents


    async def register(self):

        if self.guild_id and self.app_id:
            async with aiohttp.ClientSession() as session:
                for item in self.slash:
                    resp = await session.post(
                        f'https://discord.com/api/v9/applications/{self.app_id}/guilds/{self.guild_id}/commands',
                        json = item.json,
                        headers = self.slash_auth
                    )
                    js = await resp.json()
                    await Stack(js).slash()
                print("[ SLASH REGD ]")
        else:
            raise ValueError(
                "Application Id and Test Guild Id is mandatory to register slash command"
            )


    def start(self):

        if self.slash and self.guild_id and self.app_id:
            new_loop = asyncio.new_event_loop()
            new_loop.run_until_complete(self.register())


        ws = Websocket(
            secret = self.secret,
            prefix = self.prefix,
            bucket = self.bucket,
            intents = self.intents
        )
        loop = asyncio.new_event_loop()
        loop.run_until_complete(ws.connect())
