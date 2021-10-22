import aiohttp





class Interaction:

    def __init__(
            self,
            response: dict
    ):
        self.version = response.get('version', None)
        self.type = response.get('type', None)
        self.token = response.get('token', None)
        self.member = response.get('member', None)
        self.id = response.get('id', None)
        self.guild_id = response.get('guild_id', None)
        self.data = response.get('data', None)
        self.channel_id = response.get('channel_id', None)
        self.application_id = response.get('application_id', None)


    def __repr__(self):
        return f'{self.__dict__}'


    async def postReply(
            self,
            body: dict,
            auth: dict,
            session: aiohttp.ClientSession
    ):
        await session.post(
            f'https://discord.com/api/v9/channels/{self.channel_id}/messages',
            data = body,
            headers = auth
        )


    @property
    def slash(self):
        return int(self.data['type']) == 1


