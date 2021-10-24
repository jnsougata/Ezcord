class GuildFeatures:

    def __init__(self, features: list):
        self.__features = features


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



class Role:
    def __init__(self, cached: dict):
        self.__data = cached

    @property
    def name(self):
        return self.__data.get('name')

    @property
    def id(self):
        return self.__data.get('id')

    @property
    def color(self):
        return self.__data.get('color')

    @property
    def hoisted(self):
        return self.__data.get('hoist')

    @property
    def managed(self):
        return self.__data.get('managed')

    @property
    def mentionable(self):
        return self.__data.get('mentionable')

    @property
    def permissions(self):
        return self.__data.get("permissions")

    @property
    def position(self):
        return self.__data.get('position')

    @property
    def bot_id(self):
        tags = self.__data.get('tags')
        if tags:
            return tags.get('bot_id')

    @property
    def integration_id(self):
        tags = self.__data.get('tags')
        if tags:
            return tags.get('integration_id')

    @property
    def booster(self):
        tags = self.__data.get('tags')
        if tags:
            return tags.get('premium_subscriber')

    @property
    def emoji(self):
        return self.__data.get('unicode_emoji')

    @property
    def icon(self): #convert asset
        return self.__data.get('icon')



class Channel:

    def __init__(self, cached: dict):
        self.__data = cached
        self.__types = {
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
        key = self.__data.get('type')
        return self.__types.get(key)

    @property
    def id(self):
        return int(self.__data.get('id'))

    @property
    def name(self):
        return self.__data.get('name')

    @property
    def nfsw(self):
        return self.__data.get('nfsw')

    @property #to object
    def category(self):
        return self.__data.get('parent_id')

    @property
    def position(self):
        return self.__data.get('position')

    @property
    def overwrites(self): #to object
        return self.__data.get('permission_overwrites')

    @property
    def bitrate(self):
        return self.__data.get('bitrate')

    @property
    def rtc_region(self):
        return self.__data.get('rtc_region')

    @property
    def user_limit(self):
        return self.__data.get('user_limit')

    @property
    def latest_message(self): #to object
        return self.__data.get('last_message_id')

    @property
    def slowmode_span(self):
        return self.__data.get('rate_limit_per_user')

    @property
    def topic(self):
        return self.__data.get('topic')

    # threads pending