import json
from .embed import Embed
from .guild import Guild
from .member import Member
from .message import Message
from .channel import Channel
from aiohttp import ClientSession


class Context:

    def __init__(self, _object: dict, _cached: dict):
        self._object = _object
        self._cached = _cached
        self._secret = _object.get('_token')
        self._session = _object.get('session')
        self._author_id = _object.get('author').get('id')
        self._head = 'https://discord.com/api/v9'

    @property
    def message(self):
        return Message(self._object)

    @property
    def author(self):
        return self.guild.get_member(int(self._author_id))

    @property
    def guild(self):
        return Guild(self._cached)

    async def send(self, text: str = None, embed: Embed = None, embeds: [Embed] = None):
        if embeds:
            payload = [embed.dict() for embed in embeds]
        elif embed:
            payload = [embed.dict()]
        else:
            payload = []
        resp = await self._session.post(
            f'{self._head}/channels/{self.message.channel_id}/messages',
            json={
                'content': str(text),
                'tts': False,
                'embeds': payload,
                'components': [],
                'sticker_ids': [],
                'attachments': [],
            },
            headers={
                "Authorization": f"Bot {self._secret}",
                "Content-Type": 'application/json'
            }
        )
        return await resp.json()

    async def reply(self, text: str = None, embed: Embed = None, embeds: [Embed] = None):
        if embeds:
            payload = [embed.dict() for embed in embeds]
        elif embed:
            payload = [embed.dict()]
        else:
            payload = []
        resp = await self._session.post(
            f'{self._head}/channels/{self.message.channel_id}/messages',
            json={
                'content': str(text),
                'tts': False,
                'embeds': payload,
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
