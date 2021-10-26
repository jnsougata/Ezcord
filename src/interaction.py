import aiohttp



class Interaction:

    def __init__(
            self,
            response: dict
    ):
        self.version = response.get('version')
        self.type = response.get('type')
        self.token = response.get('token')
        self.member = response.get('member')
        self.id = response.get('id')
        self.guild_id = response.get('guild_id')
        self.data = response.get('data')
        self.channel_id = response.get('channel_id')
        self.application_id = response.get('application_id')


    def __repr__(self):
        return f'{self.__dict__}'


    async def post(
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
