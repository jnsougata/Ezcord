import json



class Guild:

    def __init__(self, Id: int):
        raw = json.load(
            open('src/stack/guild_stack.json', 'r')
        )
        self.__id = Id
        self.__data = raw[str(Id)]['d']



    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__data["name"]

    @property
    def mfa_level(self):
        return self.__data["mfa_level"]

    @property
    def large(self):
        return self.__data["large"]


    @property
    def nfsw(self):
        return self.__data["nfsw"]

    @property #convert to member object
    def owner(self):
        return self.__data["owner_id"]

    @property
    def language(self):
        return self.__data["preferred_locale"]

    @property
    def boosts(self):
        return self.__data["premium_subscription_count"]

    @property
    def boost_level(self):
        return self.__data["premium_tier"]

    @property
    def member_count(self):
        return self.__data["member_count"]

    @property
    def max_members(self):
        return self.__data["max_members"]

    @property
    def region(self):
        return self.__data["region"].upper()

    @property
    def roles(self):
        return None

    @property
    def channels(self):
        return None

    @property
    def members(self):
        return None

    @property #convert to channel obj
    def rules_channel(self):
        return self.__data["rules_channel_id"]

    @property #convert to channel obj
    def sys_channel(self):
        return self.__data["system_channel_id"]

    @property
    def vanity_code(self):
        return self.__data["vanity_url_code"]

    @property
    def verification_level(self):
        return self.__data["verification_level"]

    @property
    def nsfw_level(self):
        return self.__data["nsfw_level"]

    @property
    def icon(self): # convert to asset
        return self.__data["icon"]

    @property
    def banner(self): # convert to asset
        return self.__data["banner"]

    @property
    def features(self): # convert to object
        return self.__data["features"]

    @property
    def slash_count(self):
        return self.__data["application_command_count"]

    @property
    def emojis(self): # convert to asset
        return self.__data["emojis"]

    @property
    def content_filter(self): # convert object
        return self.__data["explicit_content_filter"]


    @property
    def alert_level(self):
        return self.__data["default_message_notifications"]

    @property
    def description(self):
        return self.__data["description"]


    def get_channel(self, id:int):
        ls = self.__data
        for item in ls:
            if item['id'] == str(id):
                return item