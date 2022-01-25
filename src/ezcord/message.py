from .embed import Embed
from .guild import Guild
from .member import Member
from aiohttp import ClientSession
from typing import List, Optional


class Message:
    def __init__(self, _object: dict):
        self.id = _object.get('id')
        self.channel_id = _object.get('channel_id')
        self.guild_id = _object.get('guild_id')
        self.author = _object.get('author')
        self.content = _object.get('content')
        self.timestamp = _object.get('timestamp')
        self.edited_timestamp = _object.get('edited_timestamp')
        self.tts = _object.get('tts')
        self.mention_everyone = _object.get('mention_everyone')
        self.mentions = _object.get('mentions')
        self.role_mentions = _object.get('mention_roles')
        self.mention_channels = _object.get('mention_channels')
        self.attachments = _object.get('attachments')
        self.embeds = _object.get('embeds')
        self.reactions = _object.get('reactions')
        self.nonce = _object.get('nonce')
        self.pinned = _object.get('pinned')
        self.webhook_id = _object.get('webhook_id')
        self.type = _object.get('type')
        self.activity = _object.get('activity')
        self.application = _object.get('application')
        self.message_reference = _object.get('message_reference')
        self.referenced_message = _object.get('referenced_message')
        self.flags = _object.get('flags')
        self.thread = _object.get('thread')
        self.components = _object.get('components')
        self.sticker_items = _object.get('sticker_items')
        self.stickers = _object.get('stickers')
        self._token = _object.get('token')
        self.client_session = _object.get('session')

    def __str__(self):
        return f"(ezcord.Message ID: {self.id})"

    async def reply(self, content: str = None, embed: Embed = None, embeds: [Embed] = None):
        if embed:
            parsed = [embed.dict()]
        elif embeds:
            parsed = [item.dict() for item in embeds]
        else:
            parsed = []
        head = 'https://discord.com/api/v9'
        resp = await self.client_session.post(
            f'{head}/channels/{self.channel.id}/messages',
            json={
                'content': str(content),
                'tts': False,
                'embeds': parsed,
                'components': [],
                'sticker_ids': [],
                'attachments': [],
                'message_reference': {
                    'message_id': self.id,
                    'channel_id': self.channel_id,
                    'guild_id': self.guild_id,
                    'fail_if_not_exists': False
                }
            },
            headers={
                "Authorization": f"Bot {self._token}",
                "Content-Type": 'application/json'
            }
        )
        return await resp.json()
