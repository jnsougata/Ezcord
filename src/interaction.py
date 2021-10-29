import aiohttp
from src.context import Member, Guild




class Interaction:

    def __init__(
            self,
            response: dict,
            guild_cache: dict,
            session: aiohttp.ClientSession,
    ):
        self.session = session,
        self._raw = response
        self.__guild_cache = guild_cache
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
        return Member(payload=self.__guild_cache['members'][str(id)])

    @property
    def version(self):
        return int(self._raw.get('version'))

    @property
    def guild(self):
        return Guild(
            Id=int(self._raw.get('guild_id')),
            payload=self.__guild_cache
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

