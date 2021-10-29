from .guild import Guild
from .member import Member


class Message:
    def __init__(self, payload:dict, guild_cache:dict):
        self.__raw_message = payload
        self.__guild_data = guild_cache

    @property
    def content(self):
        return self.__raw_message.get('content')

    @property
    def author(self):
        id = self.__raw_message['author']['id']
        return Member(self.__guild_data[str(self.guild.id)]['members'][str(id)])

    @property
    def timestamp(self): #to object
        return self.__raw_message.get('timestamp')

    @property
    def pinned(self):
        return self.__raw_message.get('pinned')

    @property
    def mentions(self): #to object
        ids = self.__raw_message.get('mentions')
        return [member for member in self.guild.members if member.id in ids]

    @property
    def role_mentions(self):
        ids = self.__raw_message.get('mention_roles')
        return [role for role in self.guild.roles if role.id in ids]

    @property
    def mentioned_everyone(self):
        return self.__raw_message.get('mention_everyone')

    @property
    def embeds(self): #to object
        return self.__raw_message.get('embeds')

    @property
    def guild(self):
        id = self.__raw_message.get('guild_id')
        return Guild(Id = id, payload=self.__guild_data)


    @property
    def channel(self):
        id = self.__raw_message.get('channel_id')
        for channel in self.guild.channels:
            if int(channel.id) == int(id):
                return channel

    @property
    def tts(self):
        return self.__raw_message.get('tts')