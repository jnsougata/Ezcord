class User:
    def __init__(self, user_id: int, user_cache: dict):
        self._user = user_cache[str(user_id)]['user']

    def __repr__(self):
        return f'{self.name}#{self.discriminator}'

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id

    @property
    def id(self):
        return int(self._user.get('id'))

    @property
    def name(self):
        return self._user.get('username')

    @property
    def discriminator(self):
        return self._user.get('discriminator')

    @property
    def flags(self):
        return self._user.get('public_flags')

    @property
    def mention(self):
        return f"<@{self.id}>"

    @property
    def avatar(self):
        base = 'https://cdn.discordapp.com/'
        return base + 'avatars' + '/' + str(self.id) + '/' + self._user.get('avatar') + '.png'
