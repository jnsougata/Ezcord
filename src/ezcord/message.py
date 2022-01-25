import aiohttp
from .embed import Embed
from .guild import Guild
from .member import Member
from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    id: int
    channel_id: int
    guild_id: int
    author: object
    member: object
    content: str
    timestamp: str
    edited_timestamp: Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: list
    mention_roles: list
    attachments: list
    embeds: list
    reactions: Optional[list]
    nonce: int
    pinned: bool
    webhook_id: Optional[int]
    type: int
    activity: object
    application: object
    application_id: Optional[int]
    message_reference: object
    flags: int
    referenced_message: object
    interaction: object
    thread: object
    components: object
    sticker_items: object
    stickers: object
    _token: str
    _session: aiohttp.ClientSession

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
        resp = await self._session.post(
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
