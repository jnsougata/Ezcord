class Role:
    def __init__(self, payload: dict):
        self._data = payload


    def __repr__(self):
        return f'<Role Object [{self.name}, {self.id}]>'


    @property
    def name(self):
        return self._data.get('name')

    @property
    def id(self):
        return self._data.get('id')

    @property
    def color(self):
        return self._data.get('color')

    @property
    def hoisted(self):
        return self._data.get('hoist')

    @property
    def managed(self):
        return self._data.get('managed')

    @property
    def mentionable(self):
        return self._data.get('mentionable')

    @property
    def permissions(self):
        return self._data.get("permissions")

    @property
    def position(self):
        return self._data.get('position')

    @property
    def bot_id(self):
        tags = self._data.get('tags')
        if tags:
            return tags.get('bot_id')

    @property
    def integration_id(self):
        tags = self._data.get('tags')
        if tags:
            return tags.get('integration_id')

    @property
    def booster(self):
        tags = self._data.get('tags')
        if tags:
            return tags.get('premium_subscriber')

    @property
    def emoji(self):
        return self._data.get('unicode_emoji')

    @property
    def icon(self): #convert asset
        return self._data.get('icon')