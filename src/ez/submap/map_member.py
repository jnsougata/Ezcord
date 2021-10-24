import json



class Member:

    def __init__(self, userId: int, guildId: int):
        cached = json.load(open('src/stack/member_stack.json', 'r'))
        self.__data: dict = cached[str(guildId)][str(userId)]




    def __repr__(self):
        return f'{self.name}#{self.discriminator}'

    @property
    def id(self):
        return int(self.__data['user']['id'])

    @property
    def name(self):
        return self.__data['user']['username']

    @property
    def nickname(self):
        return self.__data.get('nick', None)

    @property
    def any_name(self):
        if self.nickname:
            return self.nickname
        return self.name


    @property
    def discriminator(self):
        return int(self.__data["user"]['discriminator'])

    @property
    def mention(self):
        return f"<@{self.id}>"