import inspect
from src.context import Context



class Executor:

    def __init__(
            self,
            ctx: Context,
            prefix: str,
            bucket: list,
    ):
        self.ctx = ctx
        self.prefix = prefix
        self.bucket = bucket


    @property
    async def process_message(self):
        message = self.ctx.content
        if message:
            if message.startswith(self.prefix):
                string = message
                args = string.split(' ')
                cmd = args[0].replace(self.prefix,'')
                args.remove(args[0])
                args = [i for i in args if i != '']
                for item in self.bucket:
                    if item.__name__ == cmd:
                        classes = [int, str, float]
                        i = inspect.signature(item)
                        params = i.parameters
                        types = [str(params.get(key).annotation) for key in params]
                        types.remove(types[0])
                        final = []
                        for i in range(len(types)):
                            for x in classes:
                                if x.__name__ in types[i]:
                                    try:
                                        final.append(x(args[i]))
                                    except IndexError:
                                        return "Params missing"
                        val = await item.__call__(self.ctx, *final)
                        return val
                else:
                    pass