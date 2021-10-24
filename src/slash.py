import asynctube
from src.interaction import Interaction



class MakeSlash:

    def __init__(self):
        self.json = None


    def ismatched(self, index: int, value):

        TARGET = self.json["options"][index]['type']

        if TARGET == 4 and (type(value) is int):
            return True
        elif TARGET == 3 and isinstance(value, str):
            return True
        elif TARGET == 5 and (type(value) is bool):
            return True
        else:
            return None

    def command(self, name: str, description: str):

        self.json = {
            "name": name,
            "description": description,
            "type": 1,
            "options": []
        }

    def add_str_option(self, name: str, description: str, required=True):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 3,
                "required": required,
                "choices": []
            }
        )

    def add_int_option(self, name: str, description: str, required=True):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 4,
                "required": required,
                "choices": []
            }
        )

    def add_bool_option(self, name: str, description: str, required=True):
        self.json["options"].append(
            {
                "name": name,
                "description": description,
                "type": 5,
                "required": required,
                "choices": []
            }
        )

    def add_choices(self, index: int, name: str, value):

        if self.ismatched(index=index, value=value):

            self.json["options"][index]["choices"].append(
                {
                    "name": name,
                    "value": value
                }
            )
        else:
            print(index)
            raise ValueError(
                "Type of value of choice must be same as the type of option that it belongs to"
            )



class SlashReply(Interaction):

    def __init__(self, response: dict):
        super().__init__(response)


    async def callback(self, session):
        if self.slash:
            url = f'https://discord.com/api/v9/interactions/{self.id}/{self.token}/callback'
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
