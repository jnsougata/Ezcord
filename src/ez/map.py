class Author:

    def __init__(self, raw: dict):
        self._data = raw

    def __repr__(self):
        return f'{self.name}#{self.discriminator}'

    @property
    def id(self):
        return int(self._data['id'])

    @property
    def name(self):
        return self._data['username']

    @property
    def discriminator(self):
        return int(self._data['discriminator'])

    @property
    def mention(self):
        return f"<@{self.id}>"

class Member:

    def __init__(self, raw: dict):
        self._data = raw


class Tweak:

    def __init__(
            self,
            response: dict
    ):
        self.type = response.get('type', None)
        self.tts = response.get('tts', None)
        self.timestamp = response.get('timestamp', None)
        self.referenced_message = response.get('referenced_message', None)
        self.pinned = response.get('pinned', None)
        self.nonce = response.get('nonce', None)
        self.mentions = response.get('mentions', None)
        self.mention_roles = response.get('mention_roles', None)
        self.mention_everyone = response.get('mention_everyone', None)
        self.member = response.get('member', None)
        self.id = response.get('id', None)
        self.flags = response.get('flags', None)
        self.embeds = response.get('embeds', None)
        self.edited_timestamp = response.get('edited_timestamp', None)
        self.message = response.get('content', None)
        self.components = response.get('components', None)
        self.channel_id = response.get('channel_id', None)
        self.author = Author(response.get('author', None))
        self.attachments = response.get('attachments', None)
        self.guild_id = response.get('guild_id', None)



    def __repr__(self):
        return f'{self.__dict__}'

    @classmethod
    async def send(cls, text:str = None):
        return text


