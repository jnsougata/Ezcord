import inspect

class CommandParser:
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

