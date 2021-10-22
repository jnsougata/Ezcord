from src.utils.entity import Context
from src.command.parser import CommandParser


class Parser:

    def __init__(
            self,
            ctx: Context,
            prefix,
            bucket,
            secret
    ):
        self.ctx = ctx
        self.token = secret
        self.prefix = prefix
        self.bucket = bucket
        self.message = ctx.message



    async def post(
            self,
            body:dict,
            auth: dict,
            session
    ):
        await session.post(
            f'https://discord.com/api/v9/channels/{self.ctx.channel_id}/messages',
            data = body,
            headers = auth
        )


    @property
    async def process_message(self):
        if self.message:
            if self.message.startswith(self.prefix):
                args = self.message.split(' ')
                cmd = args[0].replace(self.prefix, '')
                for item in self.bucket:
                    if item.__name__ == cmd:
                        try:
                            command = CommandParser(self.message, item)
                            value = await command.execute(self.ctx)
                            if value:
                                return {'content': str(value)}
                        except:
                            return None
                else:
                    return {'content': 'Command not found'}