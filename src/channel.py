import aiohttp
from .embed import Embed


class Channel:

    def __init__(
            self,
            secret: str,
            payload: dict,
            session: aiohttp.ClientSession,
    ):
        self._types = {
            0: 'text',
            2: 'voice',
            4: 'category',
            5: 'news',
            11: 'public_thread',
            12: 'private_thread',
            13: 'stage'
        }
        self._data = payload
        self._secret = secret
        self._session = session
        self._head = 'https://discord.com/api/v9'

    @property
    def mention(self):
        return f'<#{self.id}>'

    @property
    def type(self):
        key = self._data.get('type')
        return self._types.get(key)

    @property
    def id(self):
        return int(self._data.get('id'))

    @property
    def name(self):
        return self._data.get('name')

    @property
    def nfsw(self):
        return self._data.get('nfsw')

    @property  # to object
    def category(self):
        return self._data.get('parent_id')

    @property
    def position(self):
        return self._data.get('position')

    @property
    def overwrites(self):  # to object
        return self._data.get('permission_overwrites')

    @property
    def bitrate(self):
        return self._data.get('bitrate')

    @property
    def rtc_region(self):
        return self._data.get('rtc_region')

    @property
    def user_limit(self):
        return self._data.get('user_limit')

    @property
    def latest_message(self):  # to object
        return self._data.get('last_message_id')

    @property
    def slowmode_span(self):
        return self._data.get('rate_limit_per_user')

    @property
    def topic(self):
        return self._data.get('topic')

    async def send(self, text: str = None, embeds: [Embed] = None):
        if self.type in ['text', 'news', 'public_thread', 'private_thread']:
            if embeds:
                parsed = [item.payload for item in embeds]
            else:
                parsed = []
            resp = await self._session.post(
                f'{self._head}/channels/{self.id}/messages',
                json={
                    'content': text,
                    'tts': False,
                    'embeds': parsed,
                    'components': [],
                    'sticker_ids': [],
                    'attachments': [],
                },
                headers={
                    "Authorization": f"Bot {self._secret}",
                    "Content-Type": 'application/json'
                }
            )
            return await resp.json()  # to object
        else:
            raise TypeError(f'send works on text channels only')
