import inspect



class _Parser:
    def __init__(self, string:str, func):
        self.string = string
        self.func = func



    def arg_parser(self):
        raw = self.string.split(' ')
        args = [arg for arg in raw if arg != '']
        args.remove(args[0])
        return args


    def valid_list(self):
        i = inspect.getfullargspec(self.func)
        l = len(i.args)
        param = self.arg_parser()
        return param[:l - 1]


    async def execute(self, context):
        args = self.valid_list()
        args.insert(0, context)
        return await self.func(*args)


class Executor:

    def __init__(
            self,
            ctx,
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
                            command = _Parser(self.message, item)
                            value = await command.execute(self.ctx)
                            if value:
                                return {'content': str(value)}
                        except:
                            return None
                else:
                    return {'content': 'Command not found'}