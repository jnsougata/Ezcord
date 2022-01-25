from .embed import Embed
from .guild import Guild
from .member import Member
from aiohttp import ClientSession
from typing import List, Optional


class Message:
    def __init__(self, kwargs: dict):
        self.id = kwargs.get('id')
        self.channel_id = kwargs.get('channel_id')
        self.guild_id = kwargs.get('guild_id')
        self.author = kwargs.get('author')
        self.content = kwargs.get('content')
        self.timestamp = kwargs.get('timestamp')
        self.edited_timestamp = kwargs.get('edited_timestamp')
        self.tts = kwargs.get('tts')
        self.mention_everyone = kwargs.get('mention_everyone')
        self.mentions = kwargs.get('mentions')
        self.role_mentions = kwargs.get('mention_roles')
        self.mention_channels = kwargs.get('mention_channels')
        self.attachments = kwargs.get('attachments')
        self.embeds = kwargs.get('embeds')
        self.reactions = kwargs.get('reactions')
        self.nonce = kwargs.get('nonce')
        self.pinned = kwargs.get('pinned')
        self.webhook_id = kwargs.get('webhook_id')
        self.type = kwargs.get('type')
        self.activity = kwargs.get('activity')
        self.application = kwargs.get('application')
        self.message_reference = kwargs.get('message_reference')
        self.referenced_message = kwargs.get('referenced_message')
        self.flags = kwargs.get('flags')
        self.thread = kwargs.get('thread')
        self.components = kwargs.get('components')
        self.sticker_items = kwargs.get('sticker_items')
        self.stickers = kwargs.get('stickers')
        self._token = kwargs.get('token')
        self.client_session = kwargs.get('session')

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
