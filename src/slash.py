import json
import aiohttp
from src.interaction import Interaction



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


    def add_options(self, options:list):
        self.json["options"] = options


    def subcommand(self, name: str, description: str, options: list):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 1,
                "options":options
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
            required:bool = False,
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



class _ParseSlash(Interaction):

    def __init__(self, response: dict):
        super().__init__(response)


    async def callback(self, session):
        head = 'https://discord.com/api/v9'
        if self.slash:
            url = f'{head}/interactions/{self.id}/{self.token}/callback'
            body = await self._parse()
            await session.post(url=url, json=body)


    async def _parse(self):

        if self.slash:
            data = self.data
            cmd = data['name']

            if cmd == 'embed':
                _one = data['options'][0]
                _two = data['options'][1]
                title = _one['value']
                description = _two['value']
                body = {
                    'type': 4,
                    'data': {
                        "embeds": [
                            {
                                'title': title,
                                'description': description
                            }
                        ]
                    }
                }
                return body

            elif cmd == 'echo':
                option = data['options'][0]
                phrase = option['value']
                body = {
                    'type': 4,
                    'data': {
                        "content": f'**{phrase}**'
                    }
                }
                return body

            elif cmd == 'video':
                option = data['options'][0]
                phrase = option['value']
                video = await asynctube.Search.video(phrase)
                body = {
                    'type': 4,
                    'data': {
                        "content": video.url
                    }
                }
                return body

            elif cmd == 'latency':
                hello = json.load(open("src/stack/hello_stack.json"))
                body = {
                    'type': 4,
                    'data': {
                        "content": f'**{round(hello.get("l"))} ms**'
                    }
                }
                return body

            else:
                emo = '<:warn:891339009765302302>'
                body = {
                    'type': 4,
                    'data': {
                        "embeds": [
                            {
                                'title': f'{emo} In Progress {emo}',
                                'description':
                                    f'**GitHub** [Link]'
                                    f'(https://github.com/jnsougata/ezcord)'
                                    f'\n**Dev**: Zen#8080'
                                    f'\n-----------'
                                    f'\n**Slash Info:**'
                                    f'\n**Name:** {self.data["name"]}'
                                    f'\n**Type:** {self.type}'
                                    f'\n**Version:** {self.version}'
                                    f'\n**Id:** `{self.data["id"]}`'
                            }
                        ]
                    }
                }
                return body



class SlashContext(Interaction):

    def __init__(
            self,
            response: dict,
            session: aiohttp.ClientSession
    ):
        super().__init__(response)
        self.__sess = session


    async def send(self, text: str):
        head = 'https://discord.com/api/v9'
        if self.slash:
            url = f'{head}/interactions/{self.id}/{self.token}/callback'
            body = {
                'type': 4,
                'data': {
                    "content": text
                }
            }
            await self.__sess.post(url=url, json=body)





