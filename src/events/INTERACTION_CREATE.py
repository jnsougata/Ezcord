import aiohttp


class InteractionCheck:

    def __init__(
            self,
            ctx,
            message,
            prefix,
            bucket,
            secret
    ):
        self.ctx = ctx
        self.token = secret
        self.prefix = prefix
        self.bucket = bucket
        self.message = message


    @classmethod
    async def postReply(
            cls,
            Id: str,
            body:dict,
            auth: dict,
            session: aiohttp.ClientSession
    ):
        await session.post(
            f'https://discord.com/api/v9/channels/{Id}/messages',
            data = body,
            headers = auth
        )


    @property
    async def process_message(self):
        if self.message:
            if self.message.startswith(self.prefix):
                cmd = self.message.replace(self.prefix, '')
                for item in self.bucket:
                    if item.__name__ == cmd:
                        print('CMD_INVOKED')
                        value = await item(self.ctx)
                        if value:
                            body = {'content': str(value)}
                            auth = {"Authorization": f"Bot {self.token}"}
                            return body, auth
                else:
                    body = {'content': 'Command not found'}
                    auth = {"Authorization": f"Bot {self.token}"}
                    return body, auth
            else:
                return None, None