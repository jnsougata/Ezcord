import json
from aiohttp import ClientSession


class Map:

    def __init__(
            self,
            secret: str,
            payload: dict,
            session: ClientSession
    ):
        self.__session = session
        self.__secret = secret
        self.__resp = payload
        self.__nonce = payload.get('nonce', None)
        self.__id = payload.get('id', None)
        self.__flags = payload.get('flags', None)
        self.__user_id = payload['author']['id']
        self.__guild_id = payload.get('guild_id', None)
        self.__channel_id = payload.get('channel_id', None)


    @property
    def type(self):
        return self.__resp.get('type', None)

    @property
    def tts(self):
        return self.__resp.get('tts', None)

    @property
    def timestamp(self):
        return self.__resp.get('timestamp', None)

    @property
    def referenced(self):
        return self.__resp.get('referenced_message', None)

    @property
    def pinned(self):
        return self.__resp.get('pinned', None)

    @property
    def mentions(self): # to object
        return self.__resp.get('mentions', None)

    @property
    def role_mentions(self): #to object
        return self.__resp.get('mention_roles', None)

    @property
    def everyone_mentioned(self):
        return self.__resp.get('mention_everyone', None)

    @property
    def author(self):
        return _CachedMember(
            userId = self.__user_id,
            guildId = self.__guild_id
        )

    @property
    def embeds(self):
        return self.__resp.get('embeds', None)

    @property
    def components(self):
        return self.__resp.get('components', None)

    @property
    def guild(self):
        return _CachedGuild(self.__guild_id)

    @property
    def content(self):
        return self.__resp.get('content', None)

    @property
    def edited_at(self):
        return self.__resp.get('edited_timestamp', None)

    @property
    def attachments(self):
        return self.__resp.get('attachments', None)

    @property
    def channel(self):
        id = self.__channel_id
        for item in self.guild.channels:
            if item.id == id:
                return item


    async def send(self, text: str):
        await self.__session.post(
            f'https://discord.com/api/v9/channels/{self.__channel_id}/messages',
            data = {'content': text},
            headers = {"Authorization": f"Bot {self.__secret}"}
        )
        return text


# CORE GUILD MAP
class _CachedGuild:

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
        return self.__data.get("name")

    @property
    def mfa_level(self):
        return self.__data.get("mfa_level")

    @property
    def large(self):
        return self.__data.get("large")


    @property
    def nfsw(self):
        return self.__data.get("nfsw")

    @property #convert to member object
    def owner(self):
        id = self.__data.get("owner_id")
        return _CachedMember(userId = id, guildId = self.id)

    @property
    def language(self):
        return self.__data.get("preferred_locale")

    @property
    def boosts(self):
        return self.__data.get("premium_subscription_count")

    @property
    def boost_level(self):
        return self.__data.get("premium_tier")

    @property
    def member_count(self):
        return self.__data.get("member_count")

    @property
    def max_allowed_members(self):
        return self.__data.get("max_members")

    @property
    def region(self):
        return self.__data.get("region")

    @property
    def roles(self):
        return [_CachedRole(data) for data in self.__data.get('roles')]

    @property
    def channels(self):
        return [Channel(data) for data in self.__data.get('channels')]

    @property
    def members(self):
        cached = json.load(open('src/stack/member_stack.json','r'))
        member_ids = list(cached[str(self.id)])
        return [_CachedMember(userId = Id, guildId = self.id) for Id in member_ids]

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
        return GuildFlags(self.__data.get("features"))

    @property
    def slash_count(self):
        return self.__data.get("application_command_count")

    @property
    def emojis(self): # convert to asset
        return self.__data.get("emojis")

    @property
    def content_filter(self): # convert object
        return self.__data.get("explicit_content_filter")

    @property
    def alert_level(self):
        return self.__data.get("default_message_notifications")

    @property
    def description(self):
        return self.__data.get("description")


    def pull_channel(self, id:int):
        ls = self.__data["channels"]
        for item in ls:
            if item['id'] == str(id):
                return Channel(item)

    def pull_role(self, id: int):
        ls = self.__data["roles"]
        for item in ls:
            if item['id'] == str(id):
                return _CachedRole(item)


    def pull_member(self, id:int):
        return _CachedMember(
            userId = id,
            guildId = self.id
        )


# HELPER SUB MAPS
class GuildFlags:

    def __init__(self, flags: list):
        self.__features = flags


    def __repr__(self):
        return f'<GuildFlags {self.ALL}>'


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



class _CachedRole:
    def __init__(self, payload: dict):
        self.__data = payload


    def __repr__(self):
        return f'<_CachedRole Object [{self.name}, {self.id}]>'


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


# CORE MEMBER MAP
class _CachedMember:

    def __init__(self, guildId: int):
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
