import asyncio
import aiohttp
from src.aiosocket.AioSocket import Socket
from src.slash.SlashHandler import Slash


class Bot:
    def __init__(
            self,
            token: str,
            prefix: str,
            commands: list,
            add_slash: Slash,
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
            resp = await session.post(
                f'https://discord.com/api/v9/applications/{self.slash.app_id}/guilds/{self.slash.guild_id}/commands',
                json = self.slash.json,
                headers = self.slash_auth_header
            )
            print(await resp.json())

    def start(self):
        new_loop = asyncio.new_event_loop()
        new_loop.run_until_complete(self.register())

        client = Socket(self.token)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(client.connect())
