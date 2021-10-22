import asyncio
import aiohttp
from src.slash.slashext import Slash
from src.socket.websocket import Websocket


class Bot:
    def __init__(
            self,
            token: str,
            prefix: str,
            commands: list,
            add_slash: list[Slash] = None,
    ):

        self.token = token
        self.prefix = prefix
        self.bucket = commands
        self.slash = add_slash
        self.slash_auth_header = {
            "Authorization": f"Bot {token}",
            "content-type": "application/json"
        }


    async def register(self):
        async with aiohttp.ClientSession() as session:
            for item in self.slash:
                resp = await session.post(
                    f'https://discord.com/api/v9/applications/{item.app_id}/guilds/{item.guild_id}/commands',
                    json = item.json,
                    headers = self.slash_auth_header
                )
                print(await resp.json())


    def start(self):
        if self.slash:
            new_loop = asyncio.new_event_loop()
            new_loop.run_until_complete(self.register())

        ws = Websocket(
            secret = self.token,
            prefix = self.prefix,
            bucket = self.bucket
        )
        loop = asyncio.new_event_loop()
        loop.run_until_complete(ws.connect())
