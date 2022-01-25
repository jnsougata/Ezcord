import aiohttp
from .member import Member
from typing import List, Optional


class Guild:
    def __init__(self, _object: dict):
        self.__all = _object
        self.id = int(_object.get("id")) if _object.get("id") else None
        self.name = _object.get("name")
        self.icon = _object.get("icon")
        self.splash = _object.get("splash")
        self.owner_id = _object.get("owner_id")
        self.permissions = _object.get("permissions")
        self.region = _object.get("region")
        self.afk_channel_id = _object.get("afk_channel_id")
        self.afk_timeout = _object.get("afk_timeout")
        self.embed_enabled = _object.get("embed_enabled")
        self.embed_channel_id = _object.get("embed_channel_id")
        self.verification_level = _object.get("verification_level")
        self.default_message_notifications = _object.get("default_message_notifications")
        self.explicit_content_filter = _object.get("explicit_content_filter")
        self.roles = _object.get("roles")
        self.emojis = _object.get("emojis")
        self.features = _object.get("features")
        self.mfa_level = _object.get("mfa_level")
        self.application_id = _object.get("application_id")
        self.widget_enabled = _object.get("widget_enabled")
        self.widget_channel_id = _object.get("widget_channel_id")
        self.system_channel_id = _object.get("system_channel_id")
        self.system_channel_flags = _object.get("system_channel_flags")
        self.rules_channel_id = _object.get("rules_channel_id")
        self.joined_at = _object.get("joined_at")
        self.large = _object.get("large")
        self.unavailable = _object.get("unavailable")
        self.member_count = _object.get("member_count")
        self.voice_states = _object.get("voice_states")
        self.members = _object.get("members")
        self.channels = _object.get("channels")
        self.presences = _object.get("presences")
        self.max_presences = _object.get("max_presences")
        self.max_members = _object.get("max_members")
        self.vanity_url_code = _object.get("vanity_url_code")
        self.description = _object.get("description")
        self.banner = _object.get("banner")
        self.premium_tier = _object.get("premium_tier")
        self.premium_subscription_count = _object.get("premium_subscription_count")
        self.preferred_locale = _object.get("preferred_locale")
        self.public_updates_channel_id = _object.get("public_updates_channel_id")
        self.max_video_channel_users = _object.get("max_video_channel_users")
        self.approximate_member_count = _object.get("approximate_member_count")
        self.approximate_presence_count = _object.get("approximate_presence_count")

    def owner(self):
        if self.owner_id:
            return self.get_member(int(self.owner_id))

    def get_member(self, id: int):
        return Member(self.__all.get("members").get(str(id)))

    def get_channel(self, id: int):
        return self.__all.get("channels").get(str(id))

    def get_role(self, id: int):
        return self.__all.get("roles").get(str(id))


'''class _Flags:
    ALL: list
    ANIMATED_ICON: bool
    BANNER: bool
    COMMERCE: bool
    COMMUNITY: bool
    DISCOVERABLE: bool
    FEATURABLE: bool
    INVITE_SPLASH: bool
    NEWS: bool
    PARTNERED: bool
    PREVIEW_ENABLED: bool
    PRIVATE_THREADS: bool
    ROLE_ICONS: bool
    VANITY_URL: bool
    VERIFIED: bool
    VIP_REGIONS: bool
    WELCOME_SCREEN_ENABLED: bool
    MORE_STICKERS: bool
    MONETIZED: bool
    SEVEN_DAY_THREAD_ARCHIVE: bool
    THREE_DAY_THREAD_ARCHIVE: bool
    TICKETED_EVENTS_ENABLED: bool
    SCREENING_ENABLED: bool'''
