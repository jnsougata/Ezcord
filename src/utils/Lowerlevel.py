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


