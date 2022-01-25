import aiohttp
from .role import Role
from .user import User


class Member(User):

    def __init__(self, _object: dict):
        super().__init__(_object['user'])
        self.__object = _object
        self._secret = _object.get('_token')
        self._session = _object.get('session')
        self._guild_id = _object.get('guild_id')

    @property
    def nick(self):
        return self.__object.get('nick')

    @property
    def any_name(self):
        nick = self.nickname
        return nick if nick else self.name

    @property
    def roles(self):
        ids = self.__object.get('roles')
        if ids:
            return ids

    @property
    def guild_avatar(self):
        hash_ = self.__object.get('avatar')
        if hash_:
            return f'https://cdn.discordapp.com/avatars/{str(self.guild_id)}/{hash_}.png'

    @property
    def joined_at(self):
        return self.__object.get('joined_at')

    @property
    def boosting_from(self):
        return self.__object.get('premium_since')

    @property
    def deafened(self):
        return self.__object.get('deaf')

    @property
    def muted(self):
        return self.__object.get('mute')

    @property
    def pending(self):
        return self.__object.get('pending')

    @property
    def permissions(self):
        return self.__object.get('permissions')

    @property
    def timed_out(self):
        if self.__object.get('communication_disabled_until'):
            return True

    @property
    def timeout_until(self):
        if self.__object.get('communication_disabled_until'):
            return self.__object.get('communication_disabled_until')
