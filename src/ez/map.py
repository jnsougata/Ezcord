from aiohttp import ClientSession
from src.ez.submap.map_guild import Guild
from src.ez.submap.map_member import Member



class Map:

    def __init__(
            self,
            secret: str,
            response: dict,
            session: ClientSession
    ):
        self.__session = session
        self.__secret = secret
        self.__resp = response
        self.__nonce = response.get('nonce', None)
        self.__id = response.get('id', None)
        self.__flags = response.get('flags', None)
        self.__user_id = response['author']['id']
        self.__guild_id = response.get('guild_id', None)
        self.__channel_id = response.get('channel_id', None)


    @property
    def type(self):
        return self.__resp.get('type', None)

    @property
    def tts(self):
        return self.__resp.get('tts', None)

    @property
    def timestamp(self):
        return self.__resp.get('timestamp', None)

    @property
    def referenced(self):
        return self.__resp.get('referenced_message', None)

    @property
    def pinned(self):
        return self.__resp.get('pinned', None)

    @property
    def mentions(self): # to object
        return self.__resp.get('mentions', None)

    @property
    def role_mentions(self): #to object
        return self.__resp.get('mention_roles', None)

    @property
    def everyone_mentioned(self):
        return self.__resp.get('mention_everyone', None)

    @property
    def author(self):
        return Member(
            userId = self.__user_id,
            guildId = self.__guild_id
        )

    @property
    def embeds(self):
        return self.__resp.get('embeds', None)

    @property
    def components(self):
        return self.__resp.get('components', None)

    @property
    def guild(self):
        return Guild(self.__guild_id)

    @property
    def content(self):
        return self.__resp.get('content', None)

    @property
    def edited_at(self):
        return self.__resp.get('edited_timestamp', None)

    @property
    def attachments(self):
        return self.__resp.get('attachments', None)

    @property
    def channel(self):
        id = self.__channel_id
        for item in self.guild.channels:
            if item.id == id:
                return item




    async def send(self, text: str):
        await self.__session.post(
            f'https://discord.com/api/v9/channels/{self.__channel_id}/messages',
            data = {'content': text},
            headers = {"Authorization": f"Bot {self.__secret}"}
        )
        return text
