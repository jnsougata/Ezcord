import aiohttp
from .role import Role
from .user import User
from .guild import Guild


class Member(User):

    def __init__(
            self,
            secret: str,
            user_id: int,
            guild_id: int,
            guild_cache: dict,
            session: aiohttp.ClientSession,
    ):
        super().__init__(
            user_id=user_id,
            user_cache=guild_cache[str(guild_id)]['members'],
        )
        self._secret = secret
        self._session = session
        self._guild_id = guild_id
        self._guild_cache = guild_cache
        self._member: dict = guild_cache[str(guild_id)]['members'][str(user_id)]

    @property
    def nick(self):
        return self._member.get('nick')

    @property
    def any_name(self):
        nick = self.nickname
        return nick if nick else self.name

    @property
    def roles(self):
        ids = self._member.get('roles')
        if ids:
            return [Role(self._guild_cache[str(self._guild_id)]['roles'][str(id)]) for id in ids]

    @property
    def guild_avatar(self):
        if self._member.get('avatar'):
            base = 'https://cdn.discordapp.com/'
            return base + 'avatars' + '/' + str(self._guild_id) + '/' + self._member['avatar'] + '.png'

    @property
    def guild(self):
        return Guild(
            id=self._guild_id,
            secret=self._secret,
            session=self._session,
            payload=self._guild_cache,
        )
