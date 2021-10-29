import json
from .guild import Guild
from .member import Member
from .channel import Channel
from aiohttp import ClientSession


class Context:

    def __init__(
            self,
            secret: str,
            payload: dict,
            guildcache: dict,
            session: ClientSession
    ):
        self.__resp = payload
        self.__secret = secret
        self.__session = session
        self.__id = payload.get('id')
        self.__nonce = payload.get('nonce')
        self.__flags = payload.get('flags')
        self.__user_id = payload['author']['id']
        self.__guild_id = payload.get('guild_id')
        self.__channel_id = payload.get('channel_id')
        self.__guild_data = guildcache


    @property
    def type(self):
        return self.__resp.get('type')

    @property
    def tts(self):
        return self.__resp.get('tts')

    @property
    def timestamp(self):
        return self.__resp.get('timestamp')

    @property
    def referenced(self):
        return self.__resp.get('referenced_message')

    @property
    def pinned(self):
        return self.__resp.get('pinned')

    @property
    def mentions(self): # to object
        return self.__resp.get('mentions')

    @property
    def role_mentions(self): #to object
        return self.__resp.get('mention_roles')

    @property
    def everyone_mentioned(self):
        return self.__resp.get('mention_everyone')

    @property
    def author(self):
        return Member(
            payload=self.__guild_data[str(self.__guild_id)]['members'][str(self.__user_id)]
        )

    @property
    def embeds(self):
        return self.__resp.get('embeds')

    @property
    def components(self):
        return self.__resp.get('components')

    @property
    def guild(self):
        return Guild(
            Id=self.__guild_id,
            payload=self.__guild_data
        )

    @property
    def content(self):
        return self.__resp.get('content')

    @property
    def edited_at(self):
        return self.__resp.get('edited_timestamp')

    @property
    def attachments(self):
        return self.__resp.get('attachments')

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

