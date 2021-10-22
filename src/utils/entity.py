from src.utils.sublevel import Author


class Context:

    def __init__(
            self,
            response: dict
    ):
        type = response.get('type', None)
        tts = response.get('tts', None)
        timestamp = response.get('timestamp', None)
        referenced_message = response.get('referenced_message', None)
        pinned = response.get('pinned', None)
        nonce = response.get('nonce', None)
        mentions = response.get('mentions', None)
        mention_roles = response.get('mention_roles', None)
        mention_everyone = response.get('mention_everyone', None)
        member = response.get('member', None)
        id = response.get('id', None)
        flags = response.get('flags', None)
        embeds = response.get('embeds', None)
        edited_timestamp = response.get('edited_timestamp', None)
        content = response.get('content', None)
        components = response.get('components', None)
        channel_id = response.get('channel_id', None)
        author = response.get('author', None)
        attachments = response.get('attachments', None)
        guild_id = response.get('guild_id', None)



        self.author = Author(author)
        self.channel_id = int(channel_id)
        self.edited_timestamp = edited_timestamp
        self.everyone_mention = mention_everyone
        self.components = components
        self.embeds = embeds
        self.files = attachments
        self.flags = flags
        self.guild_id = int(guild_id)
        self.id = int(id)
        self.member = member
        self.mentions = mentions
        self.message = content
        self.nonce = nonce
        self.pinned = pinned
        self.reference = referenced_message
        self.role_mentions = mention_roles
        self.timestamp = timestamp
        self.tts = tts
        self.type = type




    def __repr__(self):
        return f'{self.__dict__}'

    @classmethod
    async def send(cls, text:str = None):
        return text


