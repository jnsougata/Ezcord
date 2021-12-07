import aiohttp
from .embed import Embed
from .guild import Guild
from .member import Member


class Message:
    def __init__(
            self,
            secret: str,
            payload: dict,
            guild_cache: dict,
            session: aiohttp.ClientSession
    ):
        self._secret = secret
        self._session = session
        self.payload = payload
        self._guild_data = guild_cache

    @property
    def id(self):
        return self.payload.get('id')

    @property
    def content(self):
        return self.payload.get('content')

    @property
    def author(self):
        id = self.payload['author']['id']
        return Member(
            Id=id,
            guild_cache=self._guild_data[str(self.guild.id)]

        )

    @property
    def timestamp(self):  # to object
        return self.payload.get('timestamp')

    @property
    def pinned(self):
        return self.payload.get('pinned')

    @property
    def mentions(self):
        ids = self.payload.get('mentions')
        return [
            member for member in self.guild.members if member.id in ids
        ]

    @property
    def role_mentions(self):
        ids = self.payload.get('mention_roles')
        return [
            role for role in self.guild.roles if role.id in ids
        ]

    @property
    def mentioned_everyone(self):
        return self.payload.get('mention_everyone')

    @property
    def embeds(self):  # to object
        return self.payload.get('embeds')

    @property
    def guild(self):
        id = self.payload.get('guild_id')
        return Guild(
            Id=id,
            secret=self._secret,
            session=self._session,
            payload=self._guild_data,
        )

    @property
    def channel(self):
        id = self.payload.get('channel_id')
        for channel in self.guild.channels:
            if int(channel.id) == int(id):
                return channel

    @property
    def tts(self):
        return self.payload.get('tts')

    async def reply(self, text: str = None, embeds: [Embed] = None):
        if embeds:
            parsed = [item.payload for item in embeds]
        else:
            parsed = []
        head = 'https://discord.com/api/v9'
        resp = await self._session.post(
            f'{head}/channels/{self.channel.id}/messages',
            json={
                'content': text,
                'tts': False,
                'embeds': parsed,
                'components': [],
                'sticker_ids': [],
                'attachments': [],
                'message_reference': {
                    'message_id': self.id,
                    'channel_id': self.channel.id,
                    'guild_id': self.guild.id,
                    'fail_if_not_exists': False
                }
            },
            headers={
                "Authorization": f"Bot {self._secret}",
                "Content-Type": 'application/json'
            }
        )
        return await resp.json()
