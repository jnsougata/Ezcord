import aiohttp
from typing import List, Optional


class Guild:
    def __init__(self, kwargs: dict):
        self.__all = kwargs
        self.id = int(kwargs.get("id")) if kwargs.get("id") else None
        self.name = kwargs.get("name")
        self.icon = kwargs.get("icon")
        self.splash = kwargs.get("splash")
        self.owner_id = kwargs.get("owner_id")
        self.permissions = kwargs.get("permissions")
        self.region = kwargs.get("region")
        self.afk_channel_id = kwargs.get("afk_channel_id")
        self.afk_timeout = kwargs.get("afk_timeout")
        self.embed_enabled = kwargs.get("embed_enabled")
        self.embed_channel_id = kwargs.get("embed_channel_id")
        self.verification_level = kwargs.get("verification_level")
        self.default_message_notifications = kwargs.get("default_message_notifications")
        self.explicit_content_filter = kwargs.get("explicit_content_filter")
        self.roles = kwargs.get("roles")
        self.emojis = kwargs.get("emojis")
        self.features = kwargs.get("features")
        self.mfa_level = kwargs.get("mfa_level")
        self.application_id = kwargs.get("application_id")
        self.widget_enabled = kwargs.get("widget_enabled")
        self.widget_channel_id = kwargs.get("widget_channel_id")
        self.system_channel_id = kwargs.get("system_channel_id")
        self.system_channel_flags = kwargs.get("system_channel_flags")
        self.rules_channel_id = kwargs.get("rules_channel_id")
        self.joined_at = kwargs.get("joined_at")
        self.large = kwargs.get("large")
        self.unavailable = kwargs.get("unavailable")
        self.member_count = kwargs.get("member_count")
        self.voice_states = kwargs.get("voice_states")
        self.self.members = kwargs.get("members")
        self.channels = kwargs.get("channels")
        self.presences = kwargs.get("presences")
        self.max_presences = kwargs.get("max_presences")
        self.max_members = kwargs.get("max_members")
        self.vanity_url_code = kwargs.get("vanity_url_code")
        self.description = kwargs.get("description")
        self.banner = kwargs.get("banner")
        self.premium_tier = kwargs.get("premium_tier")
        self.premium_subscription_count = kwargs.get("premium_subscription_count")
        self.preferred_locale = kwargs.get("preferred_locale")
        self.public_updates_channel_id = kwargs.get("public_updates_channel_id")
        self.max_video_channel_users = kwargs.get("max_video_channel_users")
        self.approximate_member_count = kwargs.get("approximate_member_count")
        self.approximate_presence_count = kwargs.get("approximate_presence_count")

    def owner(self):
        return self.owner_id  # TODO: Implement this

    def get_member(self, id: int):
        return self.__all.get("members").get(str(id))

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
