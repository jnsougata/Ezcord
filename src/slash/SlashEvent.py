#import json
import asynctube
from src.utils.Interaction import Interaction


class SlashContext(Interaction):

    def __init__(self, response: dict):
        super().__init__(response)



    async def postCallback(self, session, body:dict):
        if self.slash:
            url = f'https://discord.com/api/v9/interactions/{self.id}/{self.token}/callback'
            body = body
            await session.post(url = url, json = body)


    async def buildBody(self):

        if self.slash:
            data = self.data
            cmd = data['name']

            if cmd == 'embed':
                op1 = data['options'][0]
                op2 = data['options'][1]
                title = op1['value']
                description = op2['value']
                body = {
                    'type': 4,
                    'data': {
                        "embeds":[
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
                body = {
                    'type': 4,
                    'data': {
                        "embeds": [
                            {
                                'title': 'Work in progress',
                            }
                        ]
                    }
                }
                return body