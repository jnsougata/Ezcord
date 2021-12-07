import sys
import inspect
import traceback
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
            for cmd in self.bucket:
                if cmd.__name__ == cmd_name:
                    classes = [int, str, float]
                    insp = inspect.signature(cmd)
                    dtypes = [
                        str(insp.parameters.get(key).annotation)
                        for key in insp.parameters
                    ]
                    dtypes.remove(dtypes[0])
                    # noinspection PyBroadException
                    try:
                        final = [
                            cls_(args[i])
                            for i in range(len(dtypes))
                            for cls_ in classes
                            if cls_.__name__ in dtypes[i]
                        ]
                        await cmd.__call__(self.ctx, *final)
                    except Exception:
                        traceback.print_exception(*sys.exc_info())


class SlasExec:

    def __init__(
            self,
            bucket: list,
            ctx: SlashContext,
    ):
        self.ctx = ctx
        self.bucket = bucket

    async def process_slash(self):
        cmd_name = self.ctx.data['name']
        for cmd in self.bucket:
            if cmd.__name__ == cmd_name:
                await cmd(self.ctx)
