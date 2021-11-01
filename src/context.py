import json
from .embed import Embed
from .guild import Guild
from .member import Member
from .message import Message
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
        self._raw = payload
        self._secret = secret
        self._session = session
        self._id = payload.get('id')
        self._guild_data = guildcache
        self._nonce = payload.get('nonce')
        self._flags = payload.get('flags')
        self._user_id = payload['author']['id']
        self._guild_id = payload.get('guild_id')
        self._head = 'https://discord.com/api/v9'
        self._channel_id = payload.get('channel_id')




    @property
    def message(self):
        return Message(
            secret=self._secret,
            payload=self._raw,
            session=self._session,
            guild_cache=self._guild_data,
        )


    @property
    def type(self):
        return self._raw.get('type')

    @property
    def tts(self):
        return self._raw.get('tts')

    @property
    def timestamp(self):
        return self._raw.get('timestamp')

    @property
    def referenced(self):
        return self._raw.get('referenced_message')

    @property
    def pinned(self):
        return self._raw.get('pinned')

    @property
    def mentions(self): # to object
        return self._raw.get('mentions')

    @property
    def role_mentions(self): #to object
        return self._raw.get('mention_roles')

    @property
    def everyone_mentioned(self):
        return self._raw.get('mention_everyone')

    @property
    def author(self):
        return Member(
            Id=int(self._user_id),
            guild_cache=self._guild_data[str(self._guild_id)]
        )

    @property
    def embeds(self):
        return self._raw.get('embeds')

    @property
    def components(self):
        return self._raw.get('components')

    @property
    def guild(self):
        return Guild(
            Id=self._guild_id,
            secret=self._secret,
            session=self._session,
            payload=self._guild_data,

        )

    @property
    def edited_at(self):
        return self._raw.get('edited_timestamp')

    @property
    def attachments(self):
        return self._raw.get('attachments')

    @property
    def channel(self):
        id = self._channel_id
        return Channel(
            secret=self._secret,
            session=self._session,
            payload=self._guild_data[str(self._guild_id)]['channels'][str(id)],
        )

    async def send(self, text: str = None, embeds:[Embed]  = None):
        if embeds:
            parsed = [item.payload for item in embeds]
        else:
            parsed = []
        resp = await self._session.post(
            f'{self._head}/channels/{self._channel_id}/messages',
            json = {
                'content': text,
                'tts': False,
                'embeds': parsed,
                'components': [],
                'sticker_ids': [],
                'attachments': [],
            },
            headers = {
                "Authorization": f"Bot {self._secret}",
                "Content-Type": 'application/json'
            }
        )
        return await resp.json()

    async def reply(self, text:str = None, embeds:[Embed]  = None):
        if embeds:
            parsed = [item.payload for item in embeds]
        else:
            parsed = []
        resp = await self._session.post(
            f'{self._head}/channels/{self._channel_id}/messages',
            json = {
                'content': text,
                'tts': False,
                'embeds': parsed,
                'components': [],
                'sticker_ids': [],
                'attachments': [],
                'message_reference': {
                    'message_id': self.message.id,
                    'channel_id': self._channel_id,
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

