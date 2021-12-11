import sys
import inspect
import traceback
from .cprint import Log
from .context import Context
from .slash import SlashContext


class MsgExec:

    def __init__(
            self,
            ctx: Context,
            prefix: str,
            bucket: {},
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
            cmd = self.bucket.get(cmd_name)
            if cmd:
                classes = [int, str, float]
                insp = inspect.signature(cmd)
                dtypes = [
                    str(insp.parameters.get(key).annotation)
                    for key in insp.parameters
                ]
                dtypes.remove(dtypes[0])
                try:
                    final = [
                        cls_(args[i])
                        for i in range(len(dtypes))
                        for cls_ in classes
                        if cls_.__name__ in dtypes[i]
                    ]
                    await cmd(self.ctx, *final)
                except Exception:
                    traceback.print_exception(*sys.exc_info())
            else:
                Log.red(f"[Invoked] >> {cmd_name}: command not implemented...")


class SlasExec:

    def __init__(
            self,
            bucket: dict,
            ctx: SlashContext,
    ):
        self.ctx = ctx
        self.bucket = bucket

    async def process_slash(self):
        cmd = self.bucket.get(self.ctx.data['name'])
        if cmd:
            await cmd(self.ctx)
        else:
            Log.red(f"[Invoked] >> {self.ctx.data['name']}: command not implemented...")
