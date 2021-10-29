from .role import Role
from .member import Member
from .channel import Channel




class Guild:

    def __init__(
            self,
            Id: int,
            payload: dict
    ):
        self._id = Id
        self._data: dict = payload[str(Id)]
        self._members: dict = payload[str(Id)]['members']



    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._data.get("name")

    @property
    def mfa_level(self):
        return self._data.get("mfa_level")

    @property
    def large(self):
        return self._data.get("large")


    @property
    def nfsw(self):
        return self._data.get("nfsw")

    @property
    def owner(self):
        id = self._data.get("owner_id")
        return Member(payload =self._members[str(id)])

    @property
    def language(self):
        return self._data.get("preferred_locale")

    @property
    def boosts(self):
        return self._data.get("premium_subscription_count")

    @property
    def boost_level(self):
        return self._data.get("premium_tier")

    @property
    def member_count(self):
        return self._data.get("member_count")

    @property
    def max_allowed_members(self):
        return self._data.get("max_members")

    @property
    def region(self):
        return self._data.get("region")

    @property
    def roles(self):
        return [Role(data) for data in self._data.get('roles')]

    @property
    def channels(self):
        raw = self._data.get('channels')
        return [Channel(item) for item in raw]

    @property
    def members(self):
        member_ids = list(self._members)
        return [
            Member(
                payload=self._members[str(id)]
            ) for id in member_ids]

    @property
    def rules_channel(self):
        id = self._data.get("rules_channel_id")
        payload = self._data["channels"]
        for item in payload:
            if str(item['id']) == str(id):
                return Channel(payload=item)

    @property
    def sys_channel(self):
        id = self._data.get("system_channel_id")
        payload = self._data["channels"]
        for item in payload:
            if str(item['id']) == str(id):
                return Channel(payload=item)

    @property
    def vanity_code(self):
        return self._data.get("vanity_url_code")

    @property
    def verification_level(self):
        return self._data.get("verification_level")

    @property
    def nsfw_level(self):
        return self._data.get("nsfw_level")

    @property
    def icon(self): # convert to asset
        return self._data.get("icon")

    @property
    def banner(self): # convert to asset
        return self._data.get("banner")

    @property
    def flags(self):
        return GuildFlags(self._data.get("features"))

    @property
    def slash_count(self):
        return self._data.get(
            "application_command_count"
        )

    @property
    def emojis(self): # convert to asset
        return self._data.get("emojis")

    @property
    def content_filter(self): # convert object
        return self._data.get(
            "explicit_content_filter"
        )

    @property
    def alert_level(self):
        return self._data.get(
            "default_message_notifications"
        )

    @property
    def description(self):
        return self._data.get("description")


    def pull_channel(self, id:int):
        payload = self._data["channels"]
        for item in payload:
            if str(item['id']) == str(id):
                return Channel(payload=item)


    def pull_role(self, id: int):
        ls = self._data["roles"]
        for item in ls:
            if str(item['id']) == str(id):
                return Role(item)


    def pull_member(self, id:int):
        return Member(
            payload=self._members[str(id)]
        )




class GuildFlags:

    def __init__(self, flags: list):
        self.__features = flags


    def __repr__(self):
        return f'<_GuildFlags {self.ALL}>'


    @property
    def ALL(self):
        return self.__features

    @property
    def ANIMATED(self):
        return "ANIMATED_ICON" in self.__features

    @property
    def BANNER(self):
        return "BANNER" in self.__features

    @property
    def COMMERCE(self):
        return "COMMERCE" in self.__features

    @property
    def COMMUNITY(self):
        return "COMMUNITY" in self.__features

    @property
    def DISCOVERABLE(self):
        return "DISCOVERABLE" in self.__features

    @property
    def FEATURABLE(self):
        return "FEATURABLE" in self.__features

    @property
    def INVITE_SPLASH(self):
        return "INVITE_SPLASH" in self.__features

    @property
    def NEWS(self):
        return "NEWS" in self.__features

    @property
    def PARTNERED(self):
        return "PARTNERED" in self.__features

    @property
    def PREVIEW_ENABLED(self):
        return "PREVIEW_ENABLED" in self.__features

    @property
    def PRIVATE_THREADS(self):
        return "PRIVATE_THREADS" in self.__features

    @property
    def ROLE_ICONS(self):
        return "ROLE_ICONS" in self.__features

    @property
    def VANITY_URL(self):
        return "VANITY_URL" in self.__features

    @property
    def VERIFIED(self):
        return "VERIFIED" in self.__features

    @property
    def VIP_REGIONS(self):
        return "VIP_REGIONS" in self.__features

    @property
    def WELCOME_SCREEN_ENABLED(self):
        return "WELCOME_SCREEN_ENABLED" in self.__features

    @property
    def MORE_STICKERS(self):
        return "MORE_STICKERS" in self.__features

    @property
    def MONETIZED(self):
        return "MONETIZATION_ENABLED" in self.__features

    @property
    def SEVEN_DAY_THREAD_ARCHIVE(self):
        return "SEVEN_DAY_THREAD_ARCHIVE" in self.__features

    @property
    def THREE_DAY_THREAD_ARCHIVE(self):
        return "THREE_DAY_THREAD_ARCHIVE" in self.__features

    @property
    def TICKETED_EVENTS_ENABLED(self):
        return "TICKETED_EVENTS_ENABLED" in self.__features

    @property
    def SCREENING_ENABLED(self):
        return "MEMBER_VERIFICATION_GATE_ENABLED" in self.__features