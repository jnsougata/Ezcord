from .role import Role



class Member:

    def __init__(self, Id:int, guild_cache: dict):
        self.payload = guild_cache['members'][str(Id)]
        self._roles = guild_cache['roles']
        self._data: dict = guild_cache['members'][str(Id)]


    def __repr__(self):
        return f'{self.name}#{self.discriminator}'


    @property
    def id(self):
        return int(self._data['user']['id'])

    @property
    def name(self):
        return self._data['user']['username']

    @property
    def nickname(self):
        return self._data.get('nick')

    @property
    def any_name(self):
        if self.nickname:
            return self.nickname
        return self.name

    @property
    def discriminator(self):
        return int(self._data["user"]['discriminator'])

    @property
    def mention(self):
        return f"<@{self.id}>"

    @property
    def roles(self):
        ids = self._data['roles']
        return [Role(self._roles[str(id)]) for id in ids]

    @property
    def avatar_url(self):
        base = 'https://cdn.discordapp.com/'
        url = base + 'avatars' + '/' + str(self.id) + '/' + self._data['user']['avatar'] + '.png'
        return url

    @property
    def guild_avatar_url(self):
        if self._data['avatar']:
            base = 'https://cdn.discordapp.com/'
            url = base + 'avatars' + '/' + str(self.guild_id) + '/' + self._data['avatar'] + '.png'
            return url