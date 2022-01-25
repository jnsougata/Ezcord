class User:
    def __init__(self, _object: dict):
        self.__object = _object

    def __str__(self):
        return f'{self.name}#{self.discriminator}'

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id

    @property
    def id(self):
        snowflake = self.__object.get('id')
        if snowflake:
            return int(snowflake)

    @property
    def name(self):
        return self.__object.get('username')

    @property
    def discriminator(self):
        return self.__object.get('discriminator')

    @property
    def verified(self):
        return self.__object.get('verified')

    @property
    def email(self):
        return self.__object.get('email')

    @property
    def banner(self):
        return self.__object.get('banner')

    @property
    def flags(self):
        return self.__object.get('public_flags')

    @property
    def mention(self):
        return f"<@{self.id}>"

    @property
    def avatar(self):
        return self.__object.get('avatar')

    @property
    def color(self):
        return self.__object.get('accent_color')

    @property
    def bot(self):
        return self.__object.get('bot')

    @property
    def premium_type(self):
        return self.__object.get('premium_type')

    @property
    def public_flags(self):
        return self.__object.get('public_flags')
