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
    ):
        self.ctx = ctx
        self.prefix = prefix
        self.bucket = bucket


    @property
    async def process_message(self):
        message = self.ctx.message
        if message:
            if message.startswith(self.prefix):
                args = message.split(' ')
                cmd = args[0].replace(self.prefix, '')
                for item in self.bucket:
                    if item.__name__ == cmd:
                        try:
                            command = _Parser(message, item)
                            await command.execute(self.ctx)
                        except TypeError:
                            return None
                else:
                    pass