import aiohttp
from .guild import Guild
from .member import Member
from .channel import Channel




class Interaction:

    def __init__(
            self,
            response: dict,
            guild_cache: dict,
            secret: str,
            session: aiohttp.ClientSession,
    ):
        self._session = session
        self._secret = secret
        self._raw = response
        self._guild_cache = guild_cache
        self.application_id = response.get('application_id')


    @property
    def id(self):
        return int(self._raw.get('id'))

    @property
    def data(self):
        return self._raw.get('data')

    @property
    def type(self):
        return int(self._raw.get('type'))

    @property
    def _token(self):
        return self._raw.get('token')

    @property
    def author(self):
        id = int(self._raw.get('member')['user']['id'])
        return Member(guild_cache=self._guild_cache['members'][str(id)])

    @property
    def version(self):
        return int(self._raw.get('version'))

    @property
    def guild(self):
        return Guild(
            id=int(self._raw.get('guild_id')),
            payload=self._guild_cache,
            session=self._session,
            secret=self._secret,
        )

    @property
    def channel(self):
        id = int(self._raw.get('channel_id'))
        for channel in self.guild.channels:
            if channel.id == id:
                return channel


    @property
    def slash_command(self):
        return self._raw.get('data')['type'] == 1

    @property
    def user_command(self):
        return self._raw.get('data')['type'] == 2

    @property
    def message_command(self):
        return self._raw.get('data')['type'] == 3

