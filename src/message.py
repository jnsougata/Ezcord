import aiohttp
from .guild import Guild
from .member import Member


class Message:
    def __init__(
            self,
            secret: str,
            payload:dict,
            guild_cache:dict,

            session: aiohttp.ClientSession
    ):
        self._secret = secret
        self.payload = payload
        self._session = session
        self._raw_message = payload
        self._guild_data = guild_cache

    @property
    def content(self):
        return self._raw_message.get('content')

    @property
    def author(self):
        id = self._raw_message['author']['id']
        return Member(self._guild_data[str(self.guild.id)]['members'][str(id)])

    @property
    def timestamp(self): #to object
        return self._raw_message.get('timestamp')

    @property
    def pinned(self):
        return self._raw_message.get('pinned')

    @property
    def mentions(self): #to object
        ids = self._raw_message.get('mentions')
        return [member for member in self.guild.members if member.id in ids]

    @property
    def role_mentions(self):
        ids = self._raw_message.get('mention_roles')
        return [role for role in self.guild.roles if role.id in ids]

    @property
    def mentioned_everyone(self):
        return self._raw_message.get('mention_everyone')

    @property
    def embeds(self): #to object
        return self._raw_message.get('embeds')

    @property
    def guild(self):
        id = self._raw_message.get('guild_id')
        return Guild(Id = id, payload=self._guild_data)


    @property
    def channel(self):
        id = self._raw_message.get('channel_id')
        for channel in self.guild.channels:
            if int(channel.id) == int(id):
                return channel

    @property
    def tts(self):
        return self._raw_message.get('tts')

    async def reply(self, text:str):
        head = 'https://discord.com/api/v9'
        await self._session.post(
            f'{head}/channels/{self.channel.id}/messages',
            data={'content': text},
            headers={"Authorization": f"Bot {self._secret}"}
        )
