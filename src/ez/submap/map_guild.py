import json
from src.ez.submap.map_member import Member
from src.ez.submap.map_extras import Channel, GuildFeatures

class Guild:

    def __init__(self, Id: int):
        cached = json.load(
            open('src/stack/guild_stack.json', 'r')
        )
        self.__id = Id
        self.__data: dict = cached[str(Id)]['d']



    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__data.get("name", None)

    @property
    def mfa_level(self):
        return self.__data.get("mfa_level", None)

    @property
    def large(self):
        return self.__data.get("large", None)


    @property
    def nfsw(self):
        return self.__data.get("nfsw", None)

    @property #convert to member object
    def owner(self):
        return self.__data.get("owner_id", None)

    @property
    def language(self):
        return self.__data.get("preferred_locale", None)

    @property
    def boosts(self):
        return self.__data.get("premium_subscription_count", None)

    @property
    def boost_level(self):
        return self.__data.get("premium_tier", None)

    @property
    def member_count(self):
        return self.__data.get("member_count", None)

    @property
    def max_allowed_members(self):
        return self.__data.get("max_members", None)

    @property
    def region(self):
        return self.__data.get("region", None)

    @property
    def roles(self):
        return None

    @property
    def channels(self):
        return [Channel(data) for data in self.__data.get('channels')]

    @property
    def members(self):
        return None

    @property
    def rules_channel(self):
        id = self.__data.get("rules_channel_id")
        for item in self.__data["channels"]:
            if item['id'] == id:
                return Channel(item)

    @property
    def sys_channel(self):
        id = self.__data.get("system_channel_id")
        for item in self.__data["channels"]:
            if item['id'] == id:
                return Channel(item)

    @property
    def vanity_code(self):
        return self.__data.get("vanity_url_code")

    @property
    def verification_level(self):
        return self.__data.get("verification_level")

    @property
    def nsfw_level(self):
        return self.__data.get("nsfw_level")

    @property
    def icon(self): # convert to asset
        return self.__data.get("icon")

    @property
    def banner(self): # convert to asset
        return self.__data.get("banner")

    @property
    def features(self):
        return GuildFeatures(self.__data.get("features"))

    @property
    def slash_count(self):
        return self.__data.get("application_command_count", None)

    @property
    def emojis(self): # convert to asset
        return self.__data.get("emojis", None)

    @property
    def content_filter(self): # convert object
        return self.__data.get("explicit_content_filter", None)


    @property
    def alert_level(self):
        return self.__data.get("default_message_notifications", None)

    @property
    def description(self):
        return self.__data.get("description", None)


    def pull_channel(self, id:int): #return object
        ls = self.__data["channels"]
        for item in ls:
            if item['id'] == str(id):
                return item


    def pull_member(self, id:int):
        return Member(
            userId = id,
            guildId = self.id
        )