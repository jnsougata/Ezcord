import inspect
from .context import Context
from .slash import SlashContext


class MsgExec:

    def __init__(
            self,
            ctx: Context,
            prefix: str,
            bucket: list,
    ):
        self.ctx = ctx
        self.prefix = prefix
        self.bucket = bucket

    async def process_message(self):
        message = self.ctx.message.content
        if message and message.startswith(self.prefix):
            args = message.split(' ')
            cmd_name = args[0].replace(self.prefix, '')
            args.remove(args[0])
            args = [i for i in args if i]
            for item in self.bucket:
                if item.__name__ == cmd_name:
                    classes = [int, str, float]
                    insp = inspect.signature(item)
                    types = [str(insp.parameters.get(key).annotation) for key in insp.parameters]
                    types.remove(types[0])
                    try:
                        final = [
                            cls_(args[i])
                            for i in range(len(types))
                            for cls_ in classes
                            if cls_.__name__ in types[i]
                        ]
                        try:
                            await item.__call__(self.ctx, *final)
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(f'Error occurred in command: "{cmd_name}"\nIssue: "{e}"')


class SlasExec:

    def __init__(
            self,
            bucket: list,
            ctx: SlashContext,
    ):
        self.ctx = ctx
        self.bucket = bucket

    async def process_slash(self):
        cmd = self.ctx.data['name']
        for item in self.bucket:
            if item.__name__ == cmd:
                await item(self.ctx)
