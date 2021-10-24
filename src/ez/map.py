from aiohttp import ClientSession
from src.ez.submap.map_guild import Guild
from src.ez.submap.map_author import Author



class Map:

    def __init__(
            self,
            secret: str,
            response: dict,
            session: ClientSession
    ):
        self.__session = session
        self.__secret = secret
        self.type = response.get('type', None)
        self.tts = response.get('tts', None)
        self.timestamp = response.get('timestamp', None)
        self.referenced_message = response.get('referenced_message', None)
        self.pinned = response.get('pinned', None)
        self.__nonce = response.get('nonce', None)
        self.mentions = response.get('mentions', None)
        self.mention_roles = response.get('mention_roles', None)
        self.__mention_everyone = response.get('mention_everyone', None)
        self.member = response.get('member', None)
        self.__id = response.get('id', None)
        self.flags = response.get('flags', None)
        self.embeds = response.get('embeds', None)
        self.edited_timestamp = response.get('edited_timestamp', None)
        self.message = response.get('content', None)
        self.components = response.get('components', None)
        self.channel_id = response.get('channel_id', None)
        self.author = Author(response.get('author', None))
        self.attachments = response.get('attachments', None)
        self.guild_id = response.get('guild_id', None)

    @property
    def guild(self):
        return Guild(self.guild_id)

    async def send(self, text: str):
        await self.__session.post(
            f'https://discord.com/api/v9/channels/{self.channel_id}/messages',
            data = {'content': text},
            headers = {"Authorization": f"Bot {self.__secret}"}
        )
        return text
