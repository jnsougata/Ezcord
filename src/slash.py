import json
import aiohttp
from .embed import Embed
from .context import Guild
from .interact import Interaction


class Slash:

    def __init__(self, name: str, description: str):
        self.json = {
            "name": name,
            "description": description,
            "type": 1,
            "options": [],
        }

    def _ismatched(self, index: int, value):

        TARGET = self.json["options"][index]['type']

        if TARGET == 4 and (type(value) is int):
            return True
        elif TARGET == 3 and isinstance(value, str):
            return True
        elif TARGET == 5 and (type(value) is bool):
            return True
        else:
            return None

    def add_options(self, options: list):
        self.json["options"] = options

    def subcommand(self, name: str, description: str, options: list):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 1,
                "options": options
            }
        )

    def subcommand_group(self, name: str, description: str, options: list):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 2,
                "options": options
            }
        )

    @staticmethod
    def create_subcommand(name: str, description: str):
        return {
            "name": name,
            "description": description,
            "type": 1,
        }

    @staticmethod
    def set_str_option(
            name: str,
            description: str,
            required: bool = False,
            choices: list = None,
    ):

        return {
            "name": name,
            "description": description,
            "type": 3,
            "required": required,
            "choices": choices if choices else []
        }

    @staticmethod
    def set_int_option(
            name: str,
            description: str,
            required: bool = False,
            choices: list = None,

    ):

        return {
            "name": name,
            "description": description,
            "type": 4,
            "required": required,
            "choices": choices if choices else []
        }

    @staticmethod
    def set_bool_option(
            name: str,
            description: str,
            required: bool = False,
            choices: list = None
    ):

        return {
            "name": name,
            "description": description,
            "type": 5,
            "required": required,
            "choices": choices if choices else []
        }

    @staticmethod
    def set_user_option(
            name: str,
            description: str,
            required: bool = False,
            choices: list = None,

    ):

        return {
            "name": name,
            "description": description,
            "type": 6,
            "required": required,
            "choices": choices if choices else []
        }

    @staticmethod
    def set_channel_option(
            name: str,
            description: str,
            choices: list = None,
            required: bool = False
    ):

        return {
            "name": name,
            "description": description,
            "type": 7,
            "required": required,
            "choices": choices if choices else []
        }

    @staticmethod
    def set_role_option(
            name: str,
            description: str,
            choices: list = None,
            required: bool = False
    ):

        return {
            "name": name,
            "description": description,
            "type": 8,
            "required": required,
            "choices": choices if choices else []
        }

    @staticmethod
    def set_mentionable_option(
            name: str,
            description: str,
            required: bool = False,
            choices: list = None,
    ):

        return {
            "name": name,
            "description": description,
            "type": 9,
            "required": required,
            "choices": choices if choices else []
        }

    @staticmethod
    def set_number_option(
            name: str,
            description: str,
            choices: list = None,
            required: bool = False
    ):

        return {
            "name": name,
            "description": description,
            "type": 9,
            "required": required,
            "choices": choices if choices else []
        }

    @staticmethod
    def set_choice(
            name: str,
            value
    ):

        return {
            "name": name,
            "value": value
        }


class Options:

    def __init__(self, option: dict):
        self.option = option

    def __repr__(self):
        return f'<Option {self.type} {self.value} >'

    @property
    def type(self):

        if self.option['type'] == 1:
            return 'SUB_COMMAND'

        elif self.option['type'] == 2:
            return 'SUB_COMMAND_GROUP'

        elif self.option['type'] == 3:
            return 'STRING'

        elif self.option['type'] == 4:
            return 'INTEGER'

        elif self.option['type'] == 5:
            return 'BOOLEAN'

        elif self.option['type'] == 6:
            return 'USER'

        elif self.option['type'] == 7:
            return 'CHANNEL'

        elif self.option['type'] == 8:
            return 'ROLE'

        elif self.option['type'] == 9:
            return 'MENTIONABLE'

        elif self.option['type'] == 10:
            return 'NUMBER'

    @property
    def value(self):
        return self.option['value']

    @property
    def name(self):
        return self.option['name']


class SlashContext(Interaction):

    def __init__(
            self,
            response: dict,
            bot_token: str,
            guild_cache: dict,
            session: aiohttp.ClientSession
    ):
        super().__init__(
            response=response,
            guild_cache=guild_cache,
            session=session,
            secret=bot_token,
        )
        self._session = session
        self._secret = bot_token
        self._guild_cache = guild_cache

    @property
    def options(self):
        return [Options(option) for option in self.data['options']]

    async def send(self, text: str = None, embed: Embed = None, embeds: [Embed] = None, ephemeral: bool = False):
        head = 'https://discord.com/api/v9'
        if embed:
            payload = [embed.payload]
        elif embeds:
            payload = [embed.payload for embed in embeds]
        else:
            payload = []
        if self.slash_command:
            url = f'{head}/channels/{self.channel.id}/messages'
            body = {
                "content": str(text) if text else '*empty',
                "embeds": payload,
                "flags": 64 if ephemeral else None
            }
            auth = {"Authorization": f"Bot {self._secret}"}

            await self._session.post(url=url, data=body, headers=auth)

    async def reply(self, text: str = None, embeds: list = None, ephemeral: bool = False):
        head = 'https://discord.com/api/v9'
        if self.slash_command:
            url = f'{head}/interactions/{self.id}/{self._token}/callback'
            body = {
                'type': 4,
                'data': {
                    "content": text if text else '*empty',
                    "embeds": embeds if embeds else [],
                    "flags": 64 if ephemeral else None,
                }
            }
            await self._session.post(url=url, json=body)
