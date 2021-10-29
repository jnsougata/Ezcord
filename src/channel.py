class Channel:

    def __init__(self, payload: dict):
        self._data = payload
        self._types = {
            0: 'text',
            2: 'voice',
            4: 'category',
            5: 'news',
            11: 'public_thread',
            12: 'private_thread',
            13: 'stage'
        }


    @property
    def mention(self):
        return f'<#{self.id}>'

    @property
    def type(self):
        key = self._data.get('type')
        return self._types.get(key)

    @property
    def id(self):
        return int(self._data.get('id'))

    @property
    def name(self):
        return self._data.get('name')

    @property
    def nfsw(self):
        return self._data.get('nfsw')

    @property #to object
    def category(self):
        return self._data.get('parent_id')

    @property
    def position(self):
        return self._data.get('position')

    @property
    def overwrites(self): #to object
        return self._data.get('permission_overwrites')

    @property
    def bitrate(self):
        return self._data.get('bitrate')

    @property
    def rtc_region(self):
        return self._data.get('rtc_region')

    @property
    def user_limit(self):
        return self._data.get('user_limit')

    @property
    def latest_message(self): #to object
        return self._data.get('last_message_id')

    @property
    def slowmode_span(self):
        return self._data.get('rate_limit_per_user')

    @property
    def topic(self):
        return self._data.get('topic')

    # threads pending