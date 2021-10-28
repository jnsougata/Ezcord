import json
from aiohttp import ClientSession


class Context:

    def __init__(
            self,
            secret: str,
            payload: dict,
            guildcache: dict,
            session: ClientSession
    ):
        self.__resp = payload
        self.__secret = secret
        self.__session = session
        self.__id = payload.get('id')
        self.__nonce = payload.get('nonce')
        self.__flags = payload.get('flags')
        self.__user_id = payload['author']['id']
        self.__guild_id = payload.get('guild_id')
        self.__channel_id = payload.get('channel_id')
        self.__guild_data = guildcache


    @property
    def type(self):
        return self.__resp.get('type')

    @property
    def tts(self):
        return self.__resp.get('tts')

    @property
    def timestamp(self):
        return self.__resp.get('timestamp')

    @property
    def referenced(self):
        return self.__resp.get('referenced_message')

    @property
    def pinned(self):
        return self.__resp.get('pinned')

    @property
    def mentions(self): # to object
        return self.__resp.get('mentions')

    @property
    def role_mentions(self): #to object
        return self.__resp.get('mention_roles')

    @property
    def everyone_mentioned(self):
        return self.__resp.get('mention_everyone')

    @property
    def author(self):
        return Member(
            payload=self.__guild_data[str(self.__guild_id)]['members'][str(self.__user_id)]
        )

    @property
    def embeds(self):
        return self.__resp.get('embeds')

    @property
    def components(self):
        return self.__resp.get('components')

    @property
    def guild(self):
        return Guild(
            Id=self.__guild_id,
            payload=self.__guild_data
        )

    @property
    def content(self):
        return self.__resp.get('content')

    @property
    def edited_at(self):
        return self.__resp.get('edited_timestamp')

    @property
    def attachments(self):
        return self.__resp.get('attachments')

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
        ids = [item['id'] for item in raw]
        return [
            Channel(
                payload=raw[str(id)]
            ) for id in ids
        ]

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



# HELPER SUB MAPS
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



class Role:
    def __init__(self, payload: dict):
        self._data = payload


    def __repr__(self):
        return f'<Role Object [{self.name}, {self.id}]>'


    @property
    def name(self):
        return self._data.get('name')

    @property
    def id(self):
        return self._data.get('id')

    @property
    def color(self):
        return self._data.get('color')

    @property
    def hoisted(self):
        return self._data.get('hoist')

    @property
    def managed(self):
        return self._data.get('managed')

    @property
    def mentionable(self):
        return self._data.get('mentionable')

    @property
    def permissions(self):
        return self._data.get("permissions")

    @property
    def position(self):
        return self._data.get('position')

    @property
    def bot_id(self):
        tags = self._data.get('tags')
        if tags:
            return tags.get('bot_id')

    @property
    def integration_id(self):
        tags = self._data.get('tags')
        if tags:
            return tags.get('integration_id')

    @property
    def booster(self):
        tags = self._data.get('tags')
        if tags:
            return tags.get('premium_subscriber')

    @property
    def emoji(self):
        return self._data.get('unicode_emoji')

    @property
    def icon(self): #convert asset
        return self._data.get('icon')



class Channel:

    def __init__(self, payload: dict):
        self._data = payload
        self._types = {
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
        key = self._data.get('type')
        return self._types.get(key)

    @property
    def id(self):
        return int(self._data.get('id'))

    @property
    def name(self):
        return self._data.get('name')

    @property
    def nfsw(self):
        return self._data.get('nfsw')

    @property #to object
    def category(self):
        return self._data.get('parent_id')

    @property
    def position(self):
        return self._data.get('position')

    @property
    def overwrites(self): #to object
        return self._data.get('permission_overwrites')

    @property
    def bitrate(self):
        return self._data.get('bitrate')

    @property
    def rtc_region(self):
        return self._data.get('rtc_region')

    @property
    def user_limit(self):
        return self._data.get('user_limit')

    @property
    def latest_message(self): #to object
        return self._data.get('last_message_id')

    @property
    def slowmode_span(self):
        return self._data.get('rate_limit_per_user')

    @property
    def topic(self):
        return self._data.get('topic')

    # threads pending


# CORE MEMBER MAP
class Member:

    def __init__(self, payload: dict):
        self._data: dict = payload


    def __repr__(self):
        return f'{self.name}#{self.discriminator}'


    @property
    def id(self):
        return int(self._data['user']['id'])

    @property
    def name(self):
        return self._data['user']['username']

    @property
    def nickname(self):
        return self._data.get('nick')

    @property
    def any_name(self):
        if self.nickname:
            return self.nickname
        return self.name

    @property
    def discriminator(self):
        return int(self._data["user"]['discriminator'])

    @property
    def mention(self):
        return f"<@{self.id}>"