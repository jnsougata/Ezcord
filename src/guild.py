import aiohttp
from .role import Role
from .member import Member
from .channel import Channel




class Guild:

    def __init__(
            self,
            Id: int,
            secret: str,
            payload: dict,
            session: aiohttp.ClientSession,
    ):
        self._id = Id
        self._secret = secret
        self._session = session
        self._data: dict = payload[str(Id)]



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
        return Member(Id=int(id),guild_cache=self._data)

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
        ids = list(self._data.get('roles'))
        return [Role(self._data['roles'][str(id)]) for id in ids]

    @property
    def channels(self):
        ids = list(self._data.get('channels'))
        return [
            Channel(
                secret=self._secret,
                session=self._session,
                payload=self._data['channels'][str(id)],
            ) for id in ids
        ]

    @property
    def members(self):
        member_ids = list(self._members)
        return [
            Member(
                Id=int(id),
                guild_cache=self._data
            ) for id in member_ids]

    @property
    def rules_channel(self):
        id = self._data.get("rules_channel_id")
        payload = self._data["channels"]
        return Channel(
                    payload=payload[str(id)],
                    secret=self._secret,
                    session=self._session,
                )

    @property
    def sys_channel(self):
        id = self._data.get("system_channel_id")
        payload = self._data["channels"]
        return Channel(
            payload=payload[str(id)],
            secret=self._secret,
            session=self._session,
        )

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


    @property
    def default_role(self):
        return self.roles[0]

    @property
    def top_role(self):
        ids = list(self._data.get('roles'))
        max_position = len(ids)
        roles = [self._data['roles'][str(id)] for id in ids]
        role_data = [role for role in roles if role['position'] == max_position - 1][0]
        return Role(role_data)



    def pull_channel(self, id:int):
        payload = self._data["channels"]
        return Channel(
            payload=payload[str(id)],
            secret=self._secret,
            session=self._session,
        )

    def pull_role(self, id: int):
        return Role(self._data["roles"][str(id)])


    def pull_member(self, id:int):
        return Member(
            Id=int(id),
            guild_cache=self._data
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